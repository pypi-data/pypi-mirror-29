"""Simple browser like interface for nagivating a web page and extracting
data. 

Uses requests and BeautifulSoup.
"""
from bs4 import BeautifulSoup
import requests
import logging

logger = logging.getLogger(__name__)

class Browser:
    def __init__(self, start_url):
        self._session = requests.Session()
        self._session.headers['referer'] = start_url
        self.reset()
        self.start_url = start_url

    def reset(self):
        self._response = None
        self._soup = None        

    def get(self, url, **kw):
        logger.info("GET %s", url)
        self._response = self._session.get(url, **kw)
        return self._response

    def post(self, url, data, **kw):
        logger.info("POST %s", url)
        self._response = self._session.post(url, data, **kw)
        return self._response

    def get_soup(self):
        """Returns beautiful soup of the current document."""
        if self._soup is None:
            if self._response is None:
                self.get(self.start_url)
            self._soup = BeautifulSoup(self._response.text, "lxml", from_encoding='utf8')
        return self._soup

    def get_form(self, **kw):
        form = self.get_soup().find("form", **kw)
        return form and Form(self, form)

    def read_formdata(self, inputs):
        soup = self.get_soup()
        params = {}

        for s in soup.findAll("select"):
            params[s['name']] = self.find_select_value(s)

        #params['GoogleMapForASPNet1$hidEventName'] = ''
        #params['GoogleMapForASPNet1$hidEventValue'] = ''
        params['__EVENTARGUMENT'] = ''
        params['__LASTFOCUS'] = ''
        ev = soup.find("input", {"name": "__EVENTVALIDATION"})
        if ev:
            params['__EVENTVALIDATION']  = ev['value']
        params['__VIEWSTATE'] = soup.find("input", {"name": "__VIEWSTATE"})['value']
        return params

    def get_select_options(self, name, ignore=None):
        select = self.get_soup().find("select", {"name": name})
        options = select.find_all("option")
        d = dict((o['value'], o.get_text().strip()) for o in options)

        if ignore:
            for k in ignore:
                d.pop(k, None)
        return d

class Form:
    def __init__(self, browser, form_element):
        self._browser = browser
        self._form = form_element
        self._data = None
        self.action = self._browser._response.url

    def __getitem__(self, name):
        return self.data[name]

    def __setitem__(self, name, value):
        self.data[name] = value

    def __delitem__(self, name):
        del self.data[name]

    @property
    def data(self):
        if self._data is None:
            self._data = self.get_data()
        return self._data            

    def get_data(self):
        soup = self._form
        params = {}

        for s in soup.findAll("select"):
            params[s['name']] = self.find_select_value(s) or ""

        for s in soup.findAll("input"):
            params[s['name']] = s['value'] or ""
        return params

    def find_select_value(self, select):
        if isinstance(select, basestring):
            select = self._form.find("select", {"name": select})
        option = select.find("option", {"selected": "selected"})
        return option and option.get('value')

    def submit(self):
        self._browser.post(self.action, self.data, headers={'referer': self.action})

    def __repr__(self):
        return "<Form {}>".format(self.data)