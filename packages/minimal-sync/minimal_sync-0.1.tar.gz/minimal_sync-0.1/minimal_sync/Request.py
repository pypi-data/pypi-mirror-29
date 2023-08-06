from json import dumps
import requests
from . import Rules


class Requester(object):

    def __init__(self, api_key):
        self.api_key = api_key

    def call(self, method, end_point=None, encoded=False, url=None, **options):
        if url or (method in Rules.METHODS and end_point in Rules.ENDPOINTS):
            req = getattr(requests, method)
            _url = url or (Rules.BASE_URL + Rules.ENDPOINTS[end_point])
            if options.get('token') is None:
                options.update({'api_key': self.api_key})
            if method == 'delete':
                _url += options.get('delete')
                options.pop('delete')
            if encoded:
                res = req(_url, data=dumps(options),
                          headers={'Content-type': 'application/json'})
            else:
                res = req(_url, params=options,
                          headers={'Content-type': 'application/json'})
            if res.status_code == 200:
                try:
                    return res.json()['response']
                except Exception:
                    print('an exception has occurred')
                    return res.content
        return False

    def verify_session(self, token):
        return requests.get(
            Rules.BASE_URL + 'sessions/' + token + '/verify').json()

    def verify_credentials(self, token, url):
        sts = self.call('get', url=url, token=token)
        return [status['code'] for status in sts]

