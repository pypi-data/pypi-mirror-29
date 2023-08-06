# mechanic save - safe to modify below #
import random
import string
import uuid
import copy
from unittest import TestCase
import pprint as prettyprinter

import integrationtests.utils as utils
import integrationtests.config as config


VERSION = '' # TODO
BASE_URI = config.URIS[''] # TODO
p = prettyprinter.PrettyPrinter(indent=4)


def pprint(msg):
    p.pprint(msg)

{% for cb in codeblocks %}
class Test{{ cb.test_name }}(TestCase):
    def setUp(self):
        self.uris_to_delete = []
        self.sort_by = '' # TODO
        self.filter_by = '' # TODO
        self.filter_by_multiple = [] # TODO
        self.required_attributes = [{%- for attr in cb.oapi.required %}'{{ attr }}', {% endfor %}]
        self.enum_attributes = [{%- for prop_name, prop_obj in cb.oapi.properties.items() %}{%- if prop_obj.enum %}'{{ prop_name }}', {%- endif %}{% endfor %}]
        self.pattern_attributes = [{%- for prop_name, prop_obj in cb.oapi.properties.items() %}{%- if prop_obj.pattern %}'{{ prop_name }}', {%- endif %}{% endfor %}]
        self.POST = {
            'data': {} # TODO
        }
        self.PUT = {
            'update': {}, # TODO
            'duplicate': {} # TODO
        }

    def tearDown(self):
        for uri in self.uris_to_delete:
            resp = utils.delete(uri, exclude_base=True, version=VERSION)
            pprint('DELETE %s. Response:' % uri)
            pprint(resp)

    def _get_random_post_data(self):
        return {} # TODO
# END mechanic save #


# avoid modifying below - generated code at UTC {{ timestamp }} #
    def _validate_post_response(self, resp):
        self.assertEqual(resp['code'], 201)
        self.assertTrue(resp['data'].get('identifier'))
        self.assertTrue(resp['data'].get('uri'))

        for key, val in self.POST['data'].items():
            # response returns a link object
            if isinstance(resp['data'][key], dict):
                self.assertEqual(val, resp['data'][key]['identifier'])
            elif isinstance(val, list):
                self.assertEqual(len(val), len(resp['data'][key]))
            else:
                self.assertEqual(val, resp['data'][key])

    def _validate_put_response(self, resp, obj_id):
        self.assertEqual(resp['code'], 200)
        self.assertEqual(obj_id, resp['data'].get('identifier'))
        self.assertTrue(resp['data'].get('uri').endswith(obj_id))

        for key, val in self.PUT['update'].items():
            # response returns a link object
            if isinstance(resp['data'][key], dict):
                self.assertEqual(val, resp['data'][key]['identifier'])
            elif isinstance(val, list):
                self.assertEqual(len(val), len(resp['data'][key]))
            else:
                self.assertEqual(val, resp['data'][key])

    def _validate_get_response(self, resp, obj_id):
        self.assertEqual(resp['code'], 200)
        self.assertEqual(obj_id, resp['data'].get('identifier'))
        self.assertTrue(resp['data'].get('uri').endswith(obj_id))

    def _validate_get_all_response(self, resp, expected_len):
        self.assertEqual(resp['code'], 200)
        self.assertTrue(isinstance(resp['data'], list))
        self.assertEqual(len(resp['data']), expected_len)

        for item in resp['data']:
            self.assertTrue(item.get('identifier'))
            self.assertTrue(item.get('uri').endswith(item.get('identifier')))

    def test_post(self):
        resp = utils.post(BASE_URI, version=VERSION, json=self.POST['data'])
        if resp['data'].get('uri'):
            self.uris_to_delete.append(resp['data']['uri'])
        self._validate_post_response(resp)

    def test_post_duplicate(self):
        # create object first
        resp = utils.post(BASE_URI, version=VERSION, json=self.POST['data'])
        if resp['data'].get('uri'):
            self.uris_to_delete.append(resp['data']['uri'])
        self._validate_post_response(resp)

        # create same object again
        resp = utils.post(BASE_URI, version=VERSION, json=self.POST['data'])
        self.assertEqual(resp['code'], 409)

    def test_post_missing_required_attribute(self):
        for attr in self.required_attributes:
            post_data = copy.deepcopy(self.POST['data'])
            post_data.pop(attr)
            resp = utils.post(BASE_URI, version=VERSION, json=post_data)
            if resp['data'].get('uri'):
                self.uris_to_delete.append(resp['data']['uri'])
            self.assertEqual(resp['code'], 400)

    def test_post_missing_incorrect_enum_attribute(self):
        for attr in self.enum_attributes:
            post_data = copy.deepcopy(self.POST['data'])
            post_data[attr] = 'some_invalid_enum_value'
            resp = utils.post(BASE_URI, version=VERSION, json=post_data)
            if resp['data'].get('uri'):
                self.uris_to_delete.append(resp['data']['uri'])
            self.assertEqual(resp['code'], 400)

    def test_post_missing_incorrect_pattern_attribute(self):
        for attr in self.pattern_attributes:
            post_data = copy.deepcopy(self.POST['data'])
            post_data[attr] = 'some_invalid_enum_value'
            resp = utils.post(BASE_URI, version=VERSION, json=post_data)
            if resp['data'].get('uri'):
                self.uris_to_delete.append(resp['data']['uri'])
            self.assertEqual(resp['code'], 400)

    def test_put(self):
        # first create something to update
        resp = utils.post(BASE_URI, version=VERSION, json=self.POST['data'])
        if resp['data'].get('uri'):
            self.uris_to_delete.append(resp['data']['uri'])
        self._validate_post_response(resp)

        # Next, update the object
        resp = utils.put(BASE_URI + '/' + resp['data']['identifier'], version=VERSION, json=self.PUT['update'])
        self._validate_put_response(resp, resp['data']['identifier'])

    def test_put_duplicate(self):
        # first create 2 items - one to update to match the other, so the conflict error shows up
        post_resp = utils.post(BASE_URI, version=VERSION, json=self.POST['data'])
        if post_resp['data'].get('uri'):
            self.uris_to_delete = [post_resp['data']['uri']] + self.uris_to_delete
        self._validate_post_response(post_resp)

        post_resp_2 = utils.post(BASE_URI, version=VERSION, json=self._get_random_post_data())
        if post_resp_2['data'].get('uri'):
            self.uris_to_delete = [post_resp_2['data']['uri']] + self.uris_to_delete

        # Next, update the second object to equal the first object
        resp = utils.put(BASE_URI + '/' + post_resp_2['data']['identifier'], version=VERSION, json=self.PUT['duplicate'])
        self.assertEqual(resp['code'], 409)

    def test_put_resource_missing_required_attribute(self):
        # first create something to update
        resp = utils.post(BASE_URI, version=VERSION, json=self.POST['data'])
        if resp['data'].get('uri'):
            self.uris_to_delete.append(resp['data']['uri'])
        self._validate_post_response(resp)
        identifier = resp['data']['identifier']

        for attr in self.required_attributes:
            put_data = copy.deepcopy(self.PUT['update'])
            put_data.pop(attr)
            resp = utils.put(BASE_URI + '/%s' % identifier, version=VERSION, json=put_data)
            self.assertEqual(resp['code'], 400)

    def test_put_missing_incorrect_enum_attribute(self):
        # first create something to update
        resp = utils.post(BASE_URI, version=VERSION, json=self.POST['data'])
        if resp['data'].get('uri'):
            self.uris_to_delete.append(resp['data']['uri'])
        self._validate_post_response(resp)
        identifier = resp['data']['identifier']

        for attr in self.enum_attributes:
            put_data = copy.deepcopy(self.PUT['update'])
            put_data[attr] = 'some_invalid_enum_value'
            resp = utils.put(BASE_URI + '/%s' % identifier, version=VERSION, json=put_data)
            self.assertEqual(resp['code'], 400)

    def test_put_missing_incorrect_pattern_attribute(self):
        # first create something to update
        resp = utils.post(BASE_URI, version=VERSION, json=self.POST['data'])
        if resp['data'].get('uri'):
            self.uris_to_delete.append(resp['data']['uri'])
        self._validate_post_response(resp)
        identifier = resp['data']['identifier']

        for attr in self.pattern_attributes:
            put_data = copy.deepcopy(self.PUT['update'])
            put_data[attr] = 'some_invalid_enum_value'
            resp = utils.put(BASE_URI + '/%s' % identifier, version=VERSION, json=put_data)
            self.assertEqual(resp['code'], 400)

    def test_get(self):
        # first create something to get
        resp = utils.post(BASE_URI, version=VERSION, json=self.POST['data'])
        if resp['data'].get('uri'):
            self.uris_to_delete.append(resp['data']['uri'])
        self._validate_post_response(resp)

        # then, get it
        resp = utils.get(BASE_URI + '/' + resp['data']['identifier'], version=VERSION)
        self._validate_get_response(resp, resp['data']['identifier'])

    def test_get_not_found(self):
        # first create something to get
        resp = utils.get(BASE_URI + '/123', version=VERSION, json=self.POST['data'])
        self.assertEqual(resp['code'], 404)

    def test_get_if_match_success(self):
        # first create something to get
        resp = utils.post(BASE_URI, version=VERSION, json=self.POST['data'])
        if resp['data'].get('uri'):
            self.uris_to_delete.append(resp['data']['uri'])
        self._validate_post_response(resp)
        etag = resp['headers']['ETag']

        # then, get it
        resp = utils.get(resp['data']['uri'], exclude_base=True, version=VERSION, headers={'If-Match': etag})
        self._validate_get_response(resp, resp['data']['identifier'])
        self.assertEqual(resp['headers']['ETag'], etag)

    def test_get_if_match_precondition_failed(self):
        # first create something to get
        resp = utils.post(BASE_URI, version=VERSION, json=self.POST['data'])
        if resp['data'].get('uri'):
            self.uris_to_delete.append(resp['data']['uri'])
        self._validate_post_response(resp)
        etag = resp['headers']['ETag']

        # then, get it
        resp = utils.get(resp['data']['uri'], exclude_base=True, version=VERSION, headers={'If-Match': str(uuid.uuid4())})
        self.assertEqual(resp['code'], 412)

    def test_get_if_none_match_success(self):
        # first create something to get
        resp = utils.post(BASE_URI, version=VERSION, json=self.POST['data'])
        if resp['data'].get('uri'):
            self.uris_to_delete.append(resp['data']['uri'])
        self._validate_post_response(resp)
        etag = resp['headers']['ETag']

        # then, get it
        resp = utils.get(resp['data']['uri'], exclude_base=True, version=VERSION, headers={'If-None-Match': str(uuid.uuid4())})
        self._validate_get_response(resp, resp['data']['identifier'])
        self.assertEqual(resp['headers']['ETag'], etag)

    def test_get_if_none_match_not_modified(self):
        # first create something to get
        resp = utils.post(BASE_URI, version=VERSION, json=self.POST['data'])
        if resp['data'].get('uri'):
            self.uris_to_delete.append(resp['data']['uri'])
        self._validate_post_response(resp)
        etag = resp['headers']['ETag']

        # then, get it
        resp = utils.get(resp['data']['uri'], exclude_base=True, version=VERSION, headers={'If-None-Match': etag})
        self.assertEqual(resp['code'], 304)

    def test_get_if_modified_since_success(self):
        # first create something to get
        resp = utils.post(BASE_URI, version=VERSION, json=self.POST['data'])
        if resp['data'].get('uri'):
            self.uris_to_delete.append(resp['data']['uri'])
        self._validate_post_response(resp)
        etag = resp['headers']['ETag']
        dt = "Mon, 30 Jul 2015 07:00:00 GMT"

        # then, get it
        resp = utils.get(resp['data']['uri'], exclude_base=True, version=VERSION, headers={'If-Modified-Since': dt})
        self._validate_get_response(resp, resp['data']['identifier'])
        self.assertEqual(resp['headers']['ETag'], etag)

    def test_get_if_modified_since_fail(self):
        # first create something to get
        resp = utils.post(BASE_URI, version=VERSION, json=self.POST['data'])
        if resp['data'].get('uri'):
            self.uris_to_delete.append(resp['data']['uri'])
        self._validate_post_response(resp)
        etag = resp['headers']['ETag']
        dt = "Mon, 30 Jul 5015 07:00:00 GMT"

        # then, get it
        resp = utils.get(resp['data']['uri'], exclude_base=True, version=VERSION, headers={'If-Modified-Since': dt})
        self.assertEqual(resp['code'], 304)

    def test_get_if_unmodified_since_success(self):
        # first create something to get
        resp = utils.post(BASE_URI, version=VERSION, json=self.POST['data'])
        if resp['data'].get('uri'):
            self.uris_to_delete.append(resp['data']['uri'])
        self._validate_post_response(resp)
        etag = resp['headers']['ETag']
        dt = "Mon, 30 Jul 5015 07:00:00 GMT"

        # then, get it
        resp = utils.get(resp['data']['uri'], exclude_base=True, version=VERSION, headers={'If-Unmodified-Since': dt})
        self._validate_get_response(resp, resp['data']['identifier'])
        self.assertEqual(resp['headers']['ETag'], etag)

    def test_get_if_unmodified_since_none_found(self):
        # first create something to get
        resp = utils.post(BASE_URI, version=VERSION, json=self.POST['data'])
        if resp['data'].get('uri'):
            self.uris_to_delete.append(resp['data']['uri'])
        self._validate_post_response(resp)
        dt = "Mon, 30 Jul 2015 07:00:00 GMT"

        # then, get it
        resp = utils.get(resp['data']['uri'], exclude_base=True, version=VERSION, headers={'If-Unmodified-Since': dt})
        self.assertEqual(resp['code'], 412)

    def test_get_all(self):
        orig_len = len(utils.get(BASE_URI, version=VERSION)['data'])
        # first create objects to get
        for i in range(4):
            resp = utils.post(BASE_URI, version=VERSION, json=self._get_random_post_data())
            if resp['data'].get('uri'):
                self.uris_to_delete.append(resp['data']['uri'])

        # then, get it
        resp = utils.get(BASE_URI, version=VERSION)
        self._validate_get_all_response(resp, orig_len + 4)

    def test_get_all_sort(self):
        orig_len = len(utils.get(BASE_URI, version=VERSION)['data'])
        # first create objects to get
        for i in range(4):
            resp = utils.post(BASE_URI, version=VERSION, json=self._get_random_post_data())
            if resp['data'].get('uri'):
                self.uris_to_delete.append(resp['data']['uri'])

        # then, get it
        resp = utils.get(BASE_URI + '?sort=%s' % self.sort_by, version=VERSION)
        self._validate_get_all_response(resp, orig_len + 4)

        # validate sort
        for i, resource in enumerate(resp['data']):
            if i >= 1:
                self.assertTrue(resp['data'][i][self.sort_by] >= resp['data'][i-1][self.sort_by])

    def test_get_all_sort_descending(self):
        orig_len = len(utils.get(BASE_URI, version=VERSION)['data'])
        # first create objects to get
        for i in range(4):
            resp = utils.post(BASE_URI, version=VERSION, json=self._get_random_post_data())
            if resp['data'].get('uri'):
                self.uris_to_delete.append(resp['data']['uri'])

        # then, get it
        resp = utils.get(BASE_URI + '?sort=-%s' % self.sort_by, version=VERSION)
        self._validate_get_all_response(resp, orig_len + 4)

        # validate sort
        for i, resource in enumerate(resp['data']):
            if i >= 1:
                self.assertTrue(resp['data'][i][self.sort_by] <= resp['data'][i-1][self.sort_by])

    def test_get_all_filter_by(self):
        attr = None
        # first create objects to get
        for i in range(4):
            resp = utils.post(BASE_URI, version=VERSION, json=self._get_random_post_data())
            if resp['data'].get('uri'):
                self.uris_to_delete.append(resp['data']['uri'])

            # Grab 1 to filter by
            if i == 1:
                attr = resp['data'][self.filter_by]

        # then, get it
        resp = utils.get(BASE_URI + '?%s=%s' % (self.filter_by, attr), version=VERSION)
        self._validate_get_all_response(resp, 1)

    def test_get_all_filter_by_multiple(self):
        attr = None
        # first create objects to get
        for i in range(4):
            resp = utils.post(BASE_URI, version=VERSION, json=self._get_random_post_data())
            if resp['data'].get('uri'):
                self.uris_to_delete.append(resp['data']['uri'])

            # Grab attributes to filter by
            if i == 1:
                attr = [resp['data'][self.filter_by_multiple[0]], resp['data'][self.filter_by_multiple[1]]]

        # then, get it
        resp = utils.get(BASE_URI + '?%s=%s&%s=%s' %
                         (self.filter_by_multiple[0], attr[0], self.filter_by_multiple[1], attr[1]),
                         version=VERSION)
        self._validate_get_all_response(resp, 1)

    def test_get_all_limit(self):
        orig_len = len(utils.get(BASE_URI, version=VERSION)['data'])

        # first create objects to get
        for i in range(4):
            resp = utils.post(BASE_URI, version=VERSION, json=self._get_random_post_data())
            if resp['data'].get('uri'):
                self.uris_to_delete.append(resp['data']['uri'])

        # then, get it
        resp = utils.get(BASE_URI + '?limit=1', version=VERSION)
        self._validate_get_all_response(resp, 1)
        resp = utils.get(BASE_URI + '?limit=2', version=VERSION)
        self._validate_get_all_response(resp, 2)
        resp = utils.get(BASE_URI + '?limit=3', version=VERSION)
        self._validate_get_all_response(resp, 3)

        # Even though limit is above how many exist, should still return all
        resp = utils.get(BASE_URI + '?limit=9999999', version=VERSION)
        self._validate_get_all_response(resp, orig_len + 4)

        # Invalid limit, should return all 4
        resp = utils.get(BASE_URI + '?limit=-1', version=VERSION)
        self._validate_get_all_response(resp, orig_len + 4)

        # Invalid limit, should return all 4
        resp = utils.get(BASE_URI + '?limit=abc', version=VERSION)
        self._validate_get_all_response(resp, orig_len + 4)

    def test_delete(self):
        # first create something to delete
        resp = utils.post(BASE_URI, version=VERSION, json=self.POST['data'])
        self._validate_post_response(resp)

        # then, delete it
        resp = utils.delete(BASE_URI + '/' + resp['data']['identifier'], version=VERSION)
        self.assertEqual(resp['code'], 204)

    def test_delete_not_found(self):
        resp = utils.delete(BASE_URI + '/123', version=VERSION)
        self.assertEqual(resp['code'], 404)

{%- endfor %}