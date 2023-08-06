# -*- coding: utf-8 -*-
# Copyright (c) 2013, 2017-2018 Alexander Vyushkov
# All rights reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from django.contrib.auth.models import User, Group, AnonymousUser
from django.conf import settings
import urllib
import six

from django.utils.deprecation import MiddlewareMixin

from .auth_pubtkt import Authpubtkt

class DjangoAuthPubtkt(MiddlewareMixin):
    """ Django middleware for mod_auth_pubtkt SSO """

    def __init__(self, get_response=None):
        super(DjangoAuthPubtkt, self).__init__(get_response)
        # Read configuration options from settings.py
        try:
            self.authpubtkt = Authpubtkt(settings.TKT_AUTH_PUBLIC_KEY)
        except AttributeError:
            raise AttributeError("[django-auth-pubtkt] Please specify TKT_AUTH_PUBLIC_KEY in settings.py")

        self.TKT_AUTH_COOKIE_NAME = getattr(settings, "TKT_AUTH_COOKIE_NAME", "auth_pubtkt")
        self.TKT_AUTH_USE_GROUPS = getattr(settings, "TKT_AUTH_USE_GROUPS", False)
        self.TKT_AUTH_ANONYMOUS_USER = getattr(settings, "TKT_AUTH_ANONYMOUS_USER", True)

    def add_user_to_group(self, user, group_name):
        """ Add user to a group
        """
        group, _ = Group.objects.get_or_create(name = group_name)
        group.user_set.add(user)

    def process_request(self, request):
        cookie = request.COOKIES.get(self.TKT_AUTH_COOKIE_NAME, None)
        if self.TKT_AUTH_ANONYMOUS_USER:
            request.user = AnonymousUser()

        if cookie is None:
            # User is not authenticated
            return

        if six.PY2:
            cookie = urllib.unquote(cookie)
        else:
            cookie = urllib.parse.unquote(cookie)
        params = self.authpubtkt.verify_cookie(cookie)
        if params is not None:
            username = params["uid"]
            user, _ = User.objects.get_or_create(username = username)
            request.user = user
            # Treating token as group names
            if self.TKT_AUTH_USE_GROUPS:
                user.groups.clear()
                for token in params["tokens"].split(","):
                    self.add_user_to_group(user, token)

        return None
