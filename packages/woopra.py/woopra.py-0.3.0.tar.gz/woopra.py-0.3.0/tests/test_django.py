#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for initializing the client from a Django request"""

import pytest
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User

import woopra_tracker


@pytest.fixture
def req(rf):
    r = rf.get("/", HTTP_HOST="app.acme.com", REMOTE_ADDR="127.0.0.1")
    r.user = AnonymousUser()
    yield r


def test_basic_django_setup(req):
    woopra = woopra_tracker.django(req)
    assert woopra.domain == 'app.acme.com'
    assert woopra.user == {}
    assert woopra.cookie == None
    assert woopra.ip_address == "127.0.0.1"


def test_django_with_user(req):
    """Should get email by default in the user info"""
    req.user = User(email="sally@acme.com")
    woopra = woopra_tracker.django(req)
    assert woopra.user == {'email': 'sally@acme.com'}


def test_django_custom_user_mapping(req):
    """Should be able to provide a function with a custom user data mapping"""
    req.user = User(email="sally@acme.com", first_name="Sally", last_name="V")

    def user_map(request):
        return {
            'email': request.user.email,
            'whole_name': request.user.first_name + ' ' + request.user.last_name,
        }

    woopra = woopra_tracker.django(req, user_func=user_map)
    assert woopra.user == {'email': 'sally@acme.com', 'whole_name': 'Sally V'}


def test_forwarded_ip_address(req):
    req.META['HTTP_X_FORWARDED_FOR'] = '555.0.0.1, 555.0.0.2'
    woopra = woopra_tracker.django(req)
    assert woopra.ip_address == "555.0.0.1"
