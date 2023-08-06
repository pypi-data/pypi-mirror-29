from contextlib import contextmanager
import requests
import subprocess
import json

@contextmanager
def safe_popen(*args, **kwargs):
    """Context manager that works exactly like subprocess.Popen, except that
    the process is killed at the end of the with statement.

        with safe_popen("python webapp.py 8080"):
            time.sleep(0.5) # wait for the app to start
            assert urlopen("http://localhost:8080/").code == 200
        # The webserver will be automatically killed here

    """
    p = subprocess.Popen(*args, **kwargs)
    try:
        yield p
    finally:
        p.kill()

class API:
    def __init__(self, base_url):
        self.base_url = base_url

    def request(self, method, path, data=None):
        url = self.base_url + path
        if isinstance(data, dict):
            data = json.dumps(data).encode('utf-8')
        return requests.request(method, url, data=data)

    def get(self, path):
        return self.request('GET', path)

    def post(self, path, data):
        return self.request('POST', path, data=data)

    def delete(self, path):
        return self.request('DELETE', path)

    def put(self, path, data):
        return self.request('PUT', path, data=data)

    def patch(self, path, data):
        return self.request('PATCH', path, data=data)

class Something:
    """Something is a special object that returns True
    when compared to any object except None.
    """
    def __eq__(self, other):
        return other is not None

    def __repr__(self):
        return "<Something>"

