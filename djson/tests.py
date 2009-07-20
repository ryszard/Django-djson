from django.test import TestCase
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.cache import never_cache

from decorators import login_required, ajax

try:
    import json
except ImportError:
    import simplejson as json

# never_cache is necessary because of a bug in django:
# http://code.djangoproject.com/ticket/5176
@never_cache
@login_required
def test_login(request):
    return HttpResponse('OK')

from django.conf.urls.defaults import *

urlpatterns = patterns('',
                    url(r'^login', 'jsonviews.tests.test_login', name='login'),
                    )

class JSONTest(TestCase):
    urls = 'jsonviews.tests'

    def setUp(self):
        from django.contrib.auth.models import User
        user = User.objects.create_user('user', 'user@example.com', 'password')
        user.save()

    def test_login_no_ajax(self):
        resp = self.client.get('/login')
        self.assertEqual(resp.status_code, 302)

    def test_login_ajax(self):
        resp = self.client.get('/login', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 403)
        js = json.loads(resp.content)
        self.assertEqual(js['status'], False)
        self.assertEqual(js['reason'], 'LoginRequired')
        self.assertEqual(js['next'], '/login')


    def test_login_ok_no_ajax(self):
        self.client.login(username='user', password='password')
        resp = self.client.get('/login')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'OK')

    def test_login_ok_ajax(self):
        self.client.login(username='user', password='password')
        resp = self.client.get('/login', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'OK')
