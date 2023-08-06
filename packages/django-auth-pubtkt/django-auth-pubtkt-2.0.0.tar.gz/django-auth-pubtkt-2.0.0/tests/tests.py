from django.test.testcases import TestCase
from django.http.cookie import SimpleCookie
from django.conf import settings
from django.test.utils import override_settings
from django.urls.base import reverse
import six

class MiddlewareTest(TestCase):
    def test_redirect(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, settings.LOGIN_URL + '?next=/')

    def test_expired_ticke(self):
        self.client.cookies = SimpleCookie(
            {
                'auth_pubtkt':
                    'uid=foobar;validuntil=123456789;tokens=;udata=;sig=MEUCIFqF5cxYi85Lsm0M6+1jIEb9AKX3bYa1XsH6h/ggTe6oAiEA0i3laZmjOGXJ/v9N6tt/B0PCFqOKpe7cFwegAU8GYWo='
            }
        )
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_success(self):
        # 4102444800 is 01/01/2100
        self.client.cookies = SimpleCookie(
            {
                'auth_pubtkt':
                    'uid=foobar;validuntil=4102444800;tokens=;udata=;sig=MEUCIQDPpPA1SEeXP8r/UoeNAehom31cS9/Le6eXZmokKbY7QwIgExWb6R0tPG6vKDZET0ojVnDxHoYxUx81fm+knwd0xZM='
            }
        )
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        content = response.content
        if six.PY3:
            content = content.decode("utf-8")
        self.assertEqual(content, 'User: foobar')

    def test_sso_url_no_next_parameter(self):
        self.assertRaises(RuntimeError, self.client.get, reverse('django_auth_pubtkt.sso'))

    def test_sso_url(self):
        response = self.client.get(reverse('django_auth_pubtkt.sso') + '?next=/')
        self.assertEqual(response.status_code, 302)
        # redirect url looks like '/login/?back=http%3A%2F%2Ftestserver%2F'
        url, _ = response.url.split("?", 2)
        self.assertEqual(url, settings.TKT_AUTH_LOGIN_URL)

    def test_sso_url_http(self):
        response = self.client.get(reverse('django_auth_pubtkt.sso') + '?next=http://example.com')
        self.assertEqual(response.status_code, 302)
        # redirect url looks like '/login/?back=http%3A%2F%2Ftestserver%2F'
        url, querystring = response.url.split("?", 2)
        self.assertEqual(url, settings.TKT_AUTH_LOGIN_URL)
        self.assertEqual(querystring, 'back=http%3A%2F%2Fexample.com')

    def test_sso_url_https(self):
        response = self.client.get(reverse('django_auth_pubtkt.sso') + '?next=https://example.com')
        self.assertEqual(response.status_code, 302)
        # redirect url looks like '/login/?back=http%3A%2F%2Ftestserver%2F'
        url, querystring = response.url.split("?", 2)
        self.assertEqual(url, settings.TKT_AUTH_LOGIN_URL)
        self.assertEqual(querystring, 'back=https%3A%2F%2Fexample.com')    \

    @override_settings(TKT_AUTH_BACK_ARG_NAME='haha')
    def test_sso_url_https(self):
        response = self.client.get(reverse('django_auth_pubtkt.sso') + '?next=https://example.com')
        self.assertEqual(response.status_code, 302)
        # redirect url looks like '/login/?back=http%3A%2F%2Ftestserver%2F'
        url, querystring = response.url.split("?", 2)
        self.assertEqual(url, settings.TKT_AUTH_LOGIN_URL)
        self.assertEqual(querystring, 'haha=https%3A%2F%2Fexample.com')
