# -*- coding: utf-8 -*-

"""
========================================
Woopra Python client with Django support
========================================

Client configuration
====================

At a base level, you can set up the client using keywords or a configuration
dictionary::

>>> import woopra_tracker
>>> config = {'domain': 'www.example.com'}
>>> woopra = woopra_tracker.client(**config)

User identification
===================

If you have the user information when you create the tracker instance, you can
add it then::

>>> config = {'domain': 'www.example.com'}
>>> woopra = woopra_tracker.client(user={'email': "bug@insects.com"}, **config)

To add identifying information::

>>> woopra.user['name'] = "Stick Bug"

To identify the user to Woopra::

>>> woopra.push()

Event tracking
==============

Track an event::

>>> woopra.track('purchase')

Add information to the event::

>>> woopra.track('purchase', item='Terrarium', price='50.00')

Django integration
==================

The Django client construction is a shortcut to use a an HttpRequest instance
to create the tracker.

>>> woopra = woopra_tracker.django(request)

You can pass in missing or alternative values using the keyword pattern here too::

>>> woopra = woopra_tracker.django(request, **config)

However you should be careful doing that as config values added here will *override*
values from the request.


"""
from __future__ import unicode_literals

__author__ = """Ben Lopatin"""
__email__ = 'ben@benlopatin.com'
__version__ = '0.1.0'
__license__ = 'MIT'

import requests


def get_client_ip(request):
    """

    Args:
        request:

    Returns:

    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    else:
        return request.META.get('REMOTE_ADDR')


class WoopraTracker(object):
    """
    """
    SDK_ID = "woopra.py"
    api_domain = "https://www.woopra.com"
    default_cookie_name = "wooTracker"

    def __init__(self,
                 domain=None,
                 cookie=None,
                 cookie_name=default_cookie_name,
                 idle_timeout=300000,
                 ip_address=None,
                 ignore_query_url=True,
                 user_agent=None,
                 user=None,
                 **kwargs):
        """
        Initialize the tracker instance

        Args:
            domain: the domain to be tracked
            cookie: cookie (if available)
            cookie_name: name of cookie
            idle_timeout: duration until user session considered idle (seconds)
            ip_address: IP address of the *user*
            ignore_query_url: ignore query params in page URL?
            user_agent: name of user agent
            user: dictionary of user info
            **kwargs:
        """
        if not domain:
            raise ValueError("A domain value must be provided!")

        self.domain = domain
        self.cookie = cookie
        self.cookie_name = cookie_name
        self.idle_timeout = idle_timeout
        self.ip_address = ip_address
        self.ignore_query_url = ignore_query_url
        self.user_agent = user_agent
        self.user = user or {}

        for k, v in kwargs.items():
            if not hasattr(self, k):
                setattr(self, k, v)

        self.session = requests.Session()

    def identify(self, **kwargs):
        """
        Update user dictionary with new attributes and return updated user dict

        Args:
            **kwargs: user

        Returns:
            the updated user dict

        """
        self.user.update(**kwargs)
        return self.user

    def request(self, path, **params):
        """
        General method for handling HTTP requests

        Args:
            path: the URL path fragment to request
            **params: any request parameters to include

        Returns:
            the complete API response

        """
        params.update({
            'host': self.domain,
            'ce_app': self.SDK_ID,
        })

        if self.ip_address is not None:
            params['ip'] = self.ip_address

        if self.idle_timeout is not None:
            params['timeout'] = self.idle_timeout

        if self.cookie is not None:
            params['cookie'] = self.cookie

        for k, v in self.user.items():
            params["cv_" + k] = v

        headers = {'User-agent': self.user_agent} if self.user_agent else {}

        return self.session.get(self.api_domain + path, params=params, headers=headers)

    def track(self, event_name='pv', **kwargs):
        """
        Track an event

        Args:
            event_name: identifying name
            **kwargs: event related properties

        Returns:
            the requests HTTP response

        """
        url = '/track/ce/'
        params = {'ce_{}'.format(k): v for k, v in kwargs.items()}
        return self.request(url, ce_name=event_name, **params)

    def push(self):
        """
        Sync the user information to the Woopra API

        Returns:
            the requests HTTP response

        """
        url = "/track/identify/"
        return self.request(url)


def client(**kwargs):
    """Interface for building a client instance"""
    return WoopraTracker(**kwargs)


def django(request, user_func=None, **kwargs):
    """
    Initialize a WoopraTracker instance from a Django view

    Args:
        request: the Django HttpRequest
        user_func: a callable that accepts a request and returns a dictionary;
                this is useful if you have values you want to extract from
                other field names or a user profile, for example.
        **kwargs: any additonal WoopraTracker values to set

    Returns:
        the WoopraTracker instance

    """
    if user_func:
        user = user_func(request)
    else:
        user = {
            'email': request.user.email,
        }
    default_kwargs = {
        'domain': request.META['HTTP_HOST'],
        'ip_address': get_client_ip(request),
        'cookie': request.COOKIES.get(WoopraTracker.default_cookie_name, ""),
    }
    default_kwargs.update(kwargs)
    return WoopraTracker(user=user, **default_kwargs)

