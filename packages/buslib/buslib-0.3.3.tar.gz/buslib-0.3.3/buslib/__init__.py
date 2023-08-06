import requests
import json
from . import example_objects


def parse_response(response, remove_system_keys=True):

    def process(item):
        if remove_system_keys:
            keys = list(item.keys())
            for key in keys:
                if key[0]=="_" and not key == "_id":
                    item.pop(key)
        return item

    data = response.json()

    if '_items' in data.keys():
        items = response.json()['_items']
        return list(map(lambda x: process(x), items))

    return process(data)


DEFAULT_MAX_RESULTS = 20000


class Endpoint:

    def __init__(self, session, endpoint, host="https://busmethodology-api.herokuapp.com/api", proxies="{'https' : 'https://proxy.ha.arup.com:80'}"):
        self._s = session
        self._endpoint = endpoint
        self._host = host
        self._proxies = proxies

    def _handle_error(self, response):
        try:
            data = response.json()
        except Exception:
            raise Exception(response.content)

        if '_issues' in data:
            print(data['_issues'])
        if '_items' in data:
            for item in data['_items']:
                if '_issues' in item:
                    print(item['_issues'])
        raise Exception(data['_error']['message'])

    def _kwargs_to_params(self, **kwargs):
        primitive = (int, str, bool, float)
        # jsonify non-primitive types
        params = {}
        for arg in kwargs.keys():
            if isinstance(kwargs[arg], primitive):
                params[arg] = kwargs[arg]
            else:
                params[arg] = json.dumps(kwargs[arg])

        return params

    def get(self, parse=True, remove_system_keys=True, **kwargs):
        params = self._kwargs_to_params(**kwargs)
        params['max_results'] = params.get('max_results', DEFAULT_MAX_RESULTS)
        response = self._s.get(url = self._host + '/' + self._endpoint, params=params, proxies=self._proxies)
        if response.status_code // 200 != 1:
            self._handle_error(response)

        if parse:
            return parse_response(response, remove_system_keys)
        else:
            return response

    def get_one(self, id, parse=True, remove_system_keys=True, **kwargs):
        params = self._kwargs_to_params(**kwargs)
        response = self._s.get(url = self._host + '/' + self._endpoint + '/' + id, params=params, proxies=self._proxies)
        if response.status_code // 200 != 1:
            self._handle_error(response)

        if parse:
            return parse_response(response, remove_system_keys)
        else:
            return response

    def post(self, data, parse=True, remove_system_keys=True, **kwargs):
        response = self._s.post(url = self._host + '/' + self._endpoint, json=data, proxies=self._proxies)
        if response.status_code // 200 != 1:
            self._handle_error(response)

        if parse:
            return parse_response(response, remove_system_keys)
        else:
            return response

    def patch(self, id, update):
        response = self.get_one(id, parse=False)
        if (response.status_code // 200 != 1):
            self._handle_error(response)

        etag = response.json()['_etag']
        self._s.headers['If-Match'] = etag
        response = self._s.patch(url = self._host + '/' + self._endpoint + '/' + id, json=update, proxies=self._proxies)
        self._s.headers['If-Match'] = None
        if response.status_code // 200 != 1:
            self._handle_error(response)

    def delete(self, id, **kwargs):
        response = self.get_one(id, parse=False)
        if (response.status_code // 200 != 1):
            self._handle_error(response)

        etag = response.json()['_etag']
        self._s.headers['If-Match'] = etag
        response = self._s.delete(url = self._host + '/' + self._endpoint + '/' + id)
        self._s.headers['If-Match'] = None
        if response.status_code // 200 != 1:
            self._handle_error(response)


class Client:

    def __init__(self, api_key, host="https://busmethodology-api.herokuapp.com/api", proxies="{'https' : 'https://proxy.ha.arup.com:80'}"):
        self._s = requests.Session()
        self._s.headers["Authorization"] = "Bearer %s" % api_key

        api_key
        self._host = host
        self._proxies = proxies

    @property
    def accounts(self):
        return Endpoint(self._s, 'accounts', self._host, self._proxies)

    @property
    def benchmarks(self):
        return Endpoint(self._s, 'benchmarks', self._host, self._proxies)

    @property
    def occupant_responses(self):
        return Endpoint(self._s, 'occupant_responses', self._host, self._proxies)

    @property
    def partners(self):
        return Endpoint(self._s, 'partners', self._host, self._proxies)

    @property
    def questions(self):
        return Endpoint(self._s, 'questions', self._host, self._proxies)

    @property
    def surveys(self):
        return Endpoint(self._s, 'surveys', self._host, self._proxies)

    @property
    def survey_statistics(self):
        return Endpoint(self._s, 'survey_statistics', self._host, self._proxies)
