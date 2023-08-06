import requests
import time
import uuid

log_responses = False
log_requests = False
log_waiting = False


def l(o):
    print(o)


class PfycatError(Exception):
    pass


class _Endpoints:
    _base = "https://api.gfycat.com/v1"
    token = _base + "/oauth/token"
    gfycats = _base + "/gfycats"
    status = _base + "/gfycats/fetch/status"
    users = _base + "/users"
    me = _base + "/me"
    file_drop = "https://filedrop.gfycat.com"


class Client:

    def __init__(self, client_id=None, client_secret=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        if client_id and client_secret:
            self._update_access_token()
        elif not client_id and not client_secret:
            pass
        else:
            raise PfycatError("either use both client_id AND client_secret "
                              "or neither. only one is not allowed")

    def __call__(self, *args, **kwargs):
        pass

    def me(self):
        url = _Endpoints.me
        return self._get(url)

    def users(self, name):
        return self._get(_Endpoints.users + '/' + name)

    def gfycats(self, gfy_id):
        return self._get(_Endpoints.gfycats + '/' + gfy_id)

    def upload(self, file_path, create_params=None):
        if create_params is None: create_params = {}

        create_respons = self.create_empty_gfycat(create_params)
        if not create_respons['isOk']:
            raise PfycatError('not ok', create_respons)
        # create_secret = create_respons['secret']

        gfyname = create_respons['gfyname']
        self._drop_file(gfyname, file_path)

        status = self.check_status(gfyname)

        while status["task"].lower() == "encoding":
            if log_waiting: l("encoding...")
            time.sleep(2)
            status = self.check_status(gfyname)

        if status["task"] == "complete":
            return status
        elif status["task"] == "NotFoundo":
            raise PfycatError("gfy not foundo after upload", status)
        else:
            raise PfycatError("unknown status: " + status["task"], status)

    @classmethod
    def _drop_file(cls, gfyname, file_path):
        with open(file_path, 'rb') as file:
            r = requests.put(
                _Endpoints.file_drop + "/" + gfyname,
                data=file)
        if r.status_code != 200:
            raise PfycatError("error while uploading: " + str(r.status_code) + ", " + r.text)
        if log_responses: l(r)
        return r

    def check_status(self, gfyname):
        url = _Endpoints.status + '/' + gfyname
        return self._get(url)

    def create_empty_gfycat(self, create_params=None):
        if create_params is None: create_params = {}
        url = _Endpoints.gfycats
        return self._post(url, self.access_token, json=create_params)

    @classmethod
    def _handle_result(cls, r):
        if log_responses: l(r.text)
        if r.status_code != 200:
            raise PfycatError('bad response', r.status_code, r.text)
        response = r.json()
        if 'error' in response:
            raise PfycatError(response['error'])
        return response

    def _get_auth_header(self):
        if self.access_token:
            return {"Authorization": "Bearer " + self.access_token}
        else:
            return {}

    def _get(self, url, params=None):
        r = requests.get(url, params=params, headers=self._get_auth_header())
        if r.status_code == 401 and self.access_token:
            # try again with new token
            self._update_access_token()
            r = requests.get(url, params=params, headers=self._get_auth_header())

        return self._handle_result(r)

    def _post(self, url, data=None, json=None):
        r = requests.post(url, data=data, json=json, headers=self._get_auth_header())
        if r.status_code == 401 and self.access_token:
            # try again with new token
            self._update_access_token()
            r = requests.post(url, data=data, json=json, headers=self._get_auth_header())

        return self._handle_result(r)

    def _update_access_token(self):
        params = {'grant_type': 'client_credentials',
                  'client_id': self.client_id,
                  'client_secret': self.client_secret}
        r = requests.get(_Endpoints.token, params=params)
        if r.status_code != 200:
            raise PfycatError('can\'t get oauth-token', r.status_code, r.text)
        response = r.json()
        if 'error' in response:
            raise PfycatError(response['error'])
        self.access_token = response['access_token']
