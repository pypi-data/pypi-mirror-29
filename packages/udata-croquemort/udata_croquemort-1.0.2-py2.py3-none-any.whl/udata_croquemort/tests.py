# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from datetime import datetime

import pytest
import requests

# import this first or hell will break loose
from udata.core.dataset.factories import DatasetFactory, ResourceFactory
from udata.settings import Testing
from udata.utils import faker

from .checker import CroquemortLinkChecker

CROQUEMORT_TEST_URL = 'http://check.test'
CHECK_ONE_URL = '{0}/check/one'.format(CROQUEMORT_TEST_URL)
METADATA_URL = '{0}/url'.format(CROQUEMORT_TEST_URL)


def metadata_factory(url, data=None):
    """Base for a mocked Croquemort HTTP response"""
    response = {
        'etag': '',
        'checked-url': url,
        'content-length': faker.pyint(),
        'content-disposition': '',
        'content-md5': faker.md5(),
        'content-location': '',
        'expires': faker.iso8601(),
        'final-status-code': 200,
        'updated': faker.iso8601(),
        'last-modified': faker.iso8601(),
        'content-encoding': 'gzip',
        'content-type': faker.mime_type()
    }
    if data:
        response.update(data)
    return json.dumps(response)


def mock_url_check(httpretty, url, data=None, status=200):
    url_hash = faker.md5()
    httpretty.register_uri(httpretty.POST, CHECK_ONE_URL,
                           body=json.dumps({'url-hash': url_hash}),
                           content_type='application/json')
    check_url = '/'.join((METADATA_URL, url_hash))
    httpretty.register_uri(httpretty.GET, check_url,
                           body=metadata_factory(url, data),
                           content_type='application/json',
                           status=status)


def exception_factory(exception):
    def callback(request, uri, headers):
        raise exception
    return callback


class CheckUrlSettings(Testing):
    CROQUEMORT_URL = CROQUEMORT_TEST_URL
    CROQUEMORT_NB_RETRY = 3
    CROQUEMORT_DELAY = 1


class UdataCroquemortTest:
    settings = CheckUrlSettings

    @pytest.fixture(autouse=True)
    def setup(self, app):
        self.resource = ResourceFactory()
        self.dataset = DatasetFactory(resources=[self.resource])
        self.checker = CroquemortLinkChecker()

    def test_returned_metadata(self, httpretty):
        url = self.resource.url
        test_cases = [
            {'status': 200, 'available': True},
            {'status': 301, 'available': True},
            {'status': 404, 'available': False},
            {'status': 500, 'available': False},
            {'status': 503, 'available': False},
        ]
        metadata = {
            'content-type': 'text/html; charset=utf-8',
        }
        for test_case in test_cases:
            metadata['final-status-code'] = test_case['status']
            mock_url_check(httpretty, url, metadata)
            res = self.checker.check(self.resource)
            assert res['check:url'] == url
            assert res['check:status'] == test_case['status']
            assert res['check:available'] == test_case['available']
            assert isinstance(res['check:date'], datetime)

    def test_post_request(self, httpretty):
        url = self.resource.url
        url_hash = faker.md5()
        httpretty.register_uri(httpretty.POST, CHECK_ONE_URL,
                               body=json.dumps({'url-hash': url_hash}),
                               content_type='application/json')
        check_url = '/'.join((METADATA_URL, url_hash))
        httpretty.register_uri(httpretty.GET, check_url,
                               body=metadata_factory(url),
                               content_type='application/json',
                               status=200)
        self.checker.check(self.resource)
        assert len(httpretty.core.httpretty.latest_requests)
        post_request = httpretty.core.httpretty.latest_requests[0]
        assert json.loads(post_request.body) == {
            'url': self.resource.url,
            'group': self.dataset.slug
        }

    def test_delayed_url(self, httpretty):
        url = faker.uri()
        mock_url_check(httpretty, url, status=404)
        res = self.checker.check(self.resource)
        assert res is None

    def test_timeout(self, httpretty):
        exception = requests.Timeout('Request timed out')
        httpretty.register_uri(httpretty.POST, CHECK_ONE_URL,
                               body=exception_factory(exception))
        res = self.checker.check(self.resource)
        assert res is None

    def test_connection_error(self, httpretty):
        exception = requests.ConnectionError('Unable to connect')
        httpretty.register_uri(httpretty.POST, CHECK_ONE_URL,
                               body=exception_factory(exception))
        res = self.checker.check(self.resource)
        assert res is None

    def test_json_error_check_one(self, httpretty):
        httpretty.register_uri(httpretty.POST, CHECK_ONE_URL,
                               body='<strong>not json</strong>',
                               content_type='text/html')
        res = self.checker.check(self.resource)
        assert res is None

    def test_json_error_check_url(self, httpretty):
        url_hash = faker.md5()
        httpretty.register_uri(httpretty.POST, CHECK_ONE_URL,
                               body=json.dumps({'url-hash': url_hash}),
                               content_type='application/json')
        check_url = '/'.join((METADATA_URL, url_hash))
        httpretty.register_uri(httpretty.GET, check_url,
                               body='<strong>not json</strong>',
                               content_type='text/html')
        res = self.checker.check(self.resource)
        assert res is None

    def test_retry(self, httpretty):
        '''Test the `is_pending` logic from utils.check_url'''
        url = self.resource.url
        url_hash = faker.md5()
        httpretty.register_uri(httpretty.POST, CHECK_ONE_URL,
                               body=json.dumps({'url-hash': url_hash}),
                               content_type='application/json')
        check_url = '/'.join((METADATA_URL, url_hash))

        def make_response(status, body=None):
            return httpretty.Response(body=body or metadata_factory(url),
                                      content_type='application/json',
                                      status=status)

        httpretty.register_uri(httpretty.GET, check_url,
                               responses=[
                                   make_response(500),
                                   make_response(404, body=''),
                                   make_response(200)
                               ])
        res = self.checker.check(self.resource)
        assert res['check:status'], 200


class NoCroquemortConfiguredTest:
    def test_croquemort_not_configured(self, app):
        dataset = DatasetFactory(visible=True)
        checker = CroquemortLinkChecker()

        assert checker.check(dataset.resources[0]) is None
