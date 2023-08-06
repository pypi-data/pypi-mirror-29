"""
   Copyright 2015-2017 Red Hat, Inc. and/or its affiliates
   and other contributors.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from __future__ import unicode_literals

import time
import collections
from datetime import datetime, timedelta

try:
    import simplejson as json
except ImportError:
    import json

from hawkular.client import HawkularBaseClient, HawkularError

class MetricType:
    Gauge = 'gauges'
    Availability = 'availability'
    Counter = 'counters'
    String = 'strings'
    Rate = 'rate'
    _Metrics = 'metrics'

    @staticmethod
    def short(metric_type):
        if metric_type is MetricType.Gauge:
            return 'gauge'
        elif metric_type is MetricType.Counter:
            return 'counter'
        elif metric_type is MetricType.String:
            return 'string'
        else:
            return 'availability'

class Availability:
    Down = 'down'
    Up = 'up'
    Unknown = 'unknown'

class HawkularMetricsClient(HawkularBaseClient):
    """
    Internal methods
    """
    epoch = datetime.utcfromtimestamp(0)

    def _get_url(self, metric_type=None):
        if metric_type is None:
            metric_type = MetricType._Metrics

        return self._get_base_url() + '{0}'.format(metric_type)

    def _get_metrics_single_url(self, metric_type, metric_id):
        return self._get_single_id_url(self._get_url(metric_type), metric_id)

    def _get_metrics_raw_url(self, metrics_url):
        return metrics_url + '/data' if self.legacy_api else metrics_url + '/raw'

    def _get_metrics_stats_url(self, metrics_url):
        return metrics_url + '/data' if self.legacy_api else metrics_url + '/stats'

    def _get_metrics_tags_url(self, metrics_url):
        return metrics_url + '/tags'

    def _get_tenants_url(self):
        return self._get_base_url() + 'tenants'

    def _get_status_url(self):
        return self._get_base_url() + 'status'

    def _get_single_id_url(self, previous_url, id):
        return previous_url + '/{0}'.format(HawkularBaseClient.quote(id))

    @staticmethod
    def _transform_tags(**tags):
        return ','.join("%s:%s" % (key,val) for (key,val) in tags.items())

    def _isfloat(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    """
    External methods
    """

    def tenant(self, tenant_id):
        self.tenant_id = tenant_id

    """
    Instance methods
    """

    def put(self, data):
        """
        Send multiple different metric_ids to the server in a single batch. Metrics can be a mixture
        of types.

        :param data: A dict or a list of dicts created with create_metric(metric_type, metric_id, datapoints)
        """
        if not isinstance(data, list):
            data = [data]

        r = collections.defaultdict(list)

        for d in data:
            metric_type = d.pop('type', None)
            if metric_type is None:
                raise HawkularError('Undefined MetricType')
            r[metric_type].append(d)

        # This isn't transactional, but .. ouh well. One can always repost everything.
        for l in r:
            self._post(self._get_metrics_raw_url(self._get_url(l)), r[l],parse_json=False)

    def push(self, metric_type, metric_id, value, timestamp=None):
        """
        Pushes a single metric_id, datapoint combination to the server.

        This method is an assistant method for the put method by removing the need to
        create data structures first.

        :param metric_type: MetricType to be matched (required)
        :param metric_id: Exact string matching metric id
        :param value: Datapoint value (depending on the MetricType)
        :param timestamp: Timestamp of the datapoint. If left empty, uses current client time. Can be milliseconds since epoch or datetime instance
        """
        if type(timestamp) is datetime:
            timestamp = datetime_to_time_millis(timestamp)

        item = create_metric(metric_type, metric_id, create_datapoint(value, timestamp))
        self.put(item)

    def query_metric(self, metric_type, metric_id, start=None, end=None, **query_options):
        """
        Query for metrics datapoints from the server.

        :param metric_type: MetricType to be matched (required)
        :param metric_id: Exact string matching metric id
        :param start: Milliseconds since epoch or datetime instance
        :param end: Milliseconds since epoch or datetime instance
        :param query_options: For possible query_options, see the Hawkular-Metrics documentation.
        """
        if start is not None:
            if type(start) is datetime:
                query_options['start'] = datetime_to_time_millis(start)
            else:
                query_options['start'] = start

        if end is not None:
            if type(end) is datetime:
                query_options['end'] = datetime_to_time_millis(end)
            else:
                query_options['end'] = end

        return self._get(
            self._get_metrics_raw_url(
                self._get_metrics_single_url(metric_type, metric_id)),
            **query_options)

    def query_metric_stats(self, metric_type, metric_id=None, start=None, end=None, bucketDuration=None, **query_options):
        """
        Query for metric aggregates from the server. This is called buckets in the Hawkular-Metrics documentation.

        :param metric_type: MetricType to be matched (required)
        :param metric_id: Exact string matching metric id or None for tags matching only
        :param start: Milliseconds since epoch or datetime instance
        :param end: Milliseconds since epoch or datetime instance
        :param bucketDuration: The timedelta or duration of buckets. Can be a string presentation or timedelta object
        :param query_options: For possible query_options, see the Hawkular-Metrics documentation.
        """
        if start is not None:
            if type(start) is datetime:
                query_options['start'] = datetime_to_time_millis(start)
            else:
                query_options['start'] = start

        if end is not None:
            if type(end) is datetime:
                query_options['end'] = datetime_to_time_millis(end)
            else:
                query_options['end'] = end

        if bucketDuration is not None:
            if type(bucketDuration) is timedelta:
                query_options['bucketDuration'] = timedelta_to_duration(bucketDuration)
            else:
                query_options['bucketDuration'] = bucketDuration

        if metric_id is not None:
            url = self._get_metrics_stats_url(self._get_metrics_single_url(metric_type, metric_id))
        else:
            if len(query_options) < 0:
                raise HawkularError('Tags are required when querying without metric_id')
            url = self._get_metrics_stats_url(self._get_url(metric_type))

        return self._get(url, **query_options)

    def query_metric_definition(self, metric_type, metric_id):
        """
        Query definition of a single metric id.

        :param metric_type: MetricType to be matched (required)
        :param metric_id: Exact string matching metric id
        """
        return self._get(self._get_metrics_single_url(metric_type, metric_id))

    def query_metric_definitions(self, metric_type=None, id_filter=None, **tags):
        """
        Query available metric definitions.

        :param metric_type: A MetricType to be queried. If left to None, matches all the MetricTypes
        :param id_filter: Filter the id with regexp is tag filtering is used, otherwise a list of exact metric ids
        :param tags: A dict of tag key/value pairs. Uses Hawkular-Metrics tag query language for syntax
        """
        params = {}

        if id_filter is not None:
            params['id'] = id_filter

        if metric_type is not None:
            params['type'] = MetricType.short(metric_type)

        if len(tags) > 0:
            params['tags'] = self._transform_tags(**tags)

        return self._get(self._get_url(), **params)

    def query_tag_values(self, metric_type=None, **tags):
        """
        Query for possible tag values.

        :param metric_type: A MetricType to be queried. If left to None, matches all the MetricTypes
        :param tags: A dict of tag key/value pairs. Uses Hawkular-Metrics tag query language for syntax
        """
        tagql = self._transform_tags(**tags)

        return self._get(self._get_metrics_tags_url(self._get_url(metric_type)) + '/{}'.format(tagql))

    def create_metric_definition(self, metric_type, metric_id, **tags):
        """
        Create metric definition with custom definition. **tags should be a set of tags, such as
        units, env ..

        :param metric_type: MetricType of the new definition
        :param metric_id: metric_id is the string index of the created metric
        :param tags: Key/Value tag values of the new metric
        """
        item = { 'id': metric_id }
        if len(tags) > 0:
            # We have some arguments to pass..
            data_retention = tags.pop('dataRetention', None)
            if data_retention is not None:
                item['dataRetention'] = data_retention

            if len(tags) > 0:
                item['tags'] = tags

        json_data = json.dumps(item, indent=2)
        try:
            self._post(self._get_url(metric_type), json_data)
        except HawkularError as e:
            if e.code == 409:
                return False
            raise e

        return True

    def query_metric_tags(self, metric_type, metric_id):
        """
        Returns a list of tags in the metric definition.

        :param metric_type: MetricType to be matched (required)
        :param metric_id: Exact string matching metric id
        """
        definition = self._get(self._get_metrics_tags_url(self._get_metrics_single_url(metric_type, metric_id)))
        return definition

    def update_metric_tags(self, metric_type, metric_id, **tags):
        """
        Replace the metric_id's tags with given **tags

        :param metric_type: MetricType to be matched (required)
        :param metric_id: Exact string matching metric id
        :param tags: Updated key/value tag values of the metric
        """
        self._put(self._get_metrics_tags_url(self._get_metrics_single_url(metric_type, metric_id)), tags, parse_json=False)

    def delete_metric_tags(self, metric_type, metric_id, **deleted_tags):
        """
        Delete one or more tags from the metric definition.

        :param metric_type: MetricType to be matched (required)
        :param metric_id: Exact string matching metric id
        :param deleted_tags: List of deleted tag names. Values can be set to anything
        """
        tags = self._transform_tags(**deleted_tags)
        tags_url = self._get_metrics_tags_url(self._get_metrics_single_url(metric_type, metric_id)) + '/{0}'.format(tags)

        self._delete(tags_url)

    """
    Tenant related queries
    """

    def query_tenants(self):
        """
        Query available tenants and their information.
        """
        return self._get(self._get_tenants_url())

    def create_tenant(self, tenant_id, retentions=None):
        """
        Create a tenant. Currently nothing can be set (to be fixed after the master
        version of Hawkular-Metrics has fixed implementation.

        :param retentions: A set of retention settings, see Hawkular-Metrics documentation for more info
        """
        item = { 'id': tenant_id }
        if retentions is not None:
            item['retentions'] = retentions

        self._post(self._get_tenants_url(), json.dumps(item, indent=2))

    def delete_tenant(self, tenant_id):
        """
        Asynchronously deletes a tenant and all the data associated with the tenant.
        :param tenant_id: Tenant id to be sent for deletion process
        """
        self._delete(self._get_single_id_url(self._get_tenants_url(), tenant_id))

"""
Static methods
"""
def time_millis():
    """
    Returns current milliseconds since epoch
    """
    return int(round(time.time() * 1000))

def timedelta_to_duration(td):
    return '{}s'.format(int(td.total_seconds()))

def datetime_to_time_millis(dt):
    return '{:.0f}'.format((dt - HawkularMetricsClient.epoch).total_seconds() * 1000)

def create_datapoint(value, timestamp=None, **tags):
    """
    Creates a single datapoint dict with a value, timestamp and tags.

    :param value: Value of the datapoint. Type depends on the id's MetricType
    :param timestamp: Optional timestamp of the datapoint. Uses client current time if not set. Millisecond accuracy. Can be datetime instance also.
    :param tags: Optional datapoint tags. Not to be confused with metric definition tags
    """
    if timestamp is None:
        timestamp = time_millis()

    if type(timestamp) is datetime:
        timestamp = datetime_to_time_millis(timestamp)

    item = { 'timestamp': timestamp,
             'value': value }

    if tags is not None:
        item['tags'] = tags

    return item

def create_metric(metric_type, metric_id, data):
    """
    Create Hawkular-Metrics' submittable structure.

    :param metric_type: MetricType to be matched (required)
    :param metric_id: Exact string matching metric id
    :param data: A datapoint or a list of datapoints created with create_datapoint(value, timestamp, tags)
    """
    if not isinstance(data, list):
        data = [data]

    return { 'type': metric_type,'id': metric_id, 'data': data }

def create_percentiles_filter(*percentiles):
    """
    Create percentiles filter from a list of float64 percentile values
    """
    return ','.join("%s" % p for p in percentiles)

def create_tags_filter(**tags):
    """
    Transform a set of parameters to a tag query language filter
    """
    return HawkularMetricsClient._transform_tags(**tags)
