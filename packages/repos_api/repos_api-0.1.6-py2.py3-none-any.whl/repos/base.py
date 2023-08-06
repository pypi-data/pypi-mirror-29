#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Repos API
# Copyright (c) 2008-2018 Hive Solutions Lda.
#
# This file is part of Hive Repos API.
#
# Hive Repos API is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Repos API is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Repos API. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2018 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import appier

from . import package

BASE_URL = "https://repos.bemisc.com/"
""" The default base URL to be used when no other
base URL value is provided to the constructor """

class API(
    appier.API,
    package.PackageAPI
):

    def __init__(self, *args, **kwargs):
        appier.API.__init__(self, *args, **kwargs)
        self.base_url = appier.conf("REPOS_BASE_URL", BASE_URL)
        self.username = appier.conf("REPOS_USERNAME", None)
        self.password = appier.conf("REPOS_PASSWORD", None)
        self.base_url = kwargs.get("base_url", self.base_url)
        self.username = kwargs.get("username", self.username)
        self.password = kwargs.get("password", self.password)
        self.session_id = kwargs.get("session_id", None)

    def build(
        self,
        method,
        url,
        data = None,
        data_j = None,
        data_m = None,
        headers = None,
        params = None,
        mime = None,
        kwargs = None
    ):
        auth = kwargs.pop("auth", True)
        if auth: params["sid"] = self.get_session_id()

    def get_session_id(self):
        if self.session_id: return self.session_id
        return self.login()

    def auth_callback(self, params, headers):
        self.session_id = None
        session_id = self.get_session_id()
        params["session_id"] = session_id

    def login(self, username = None, password = None):
        username = username or self.username
        password = password or self.password
        url = self.base_url + "api/admin/login"
        contents = self.post(
            url,
            callback = False,
            auth = False,
            username = username,
            password = password
        )
        self.session_id = contents.get("session_id", None)
        self.tokens = contents.get("tokens", None)
        self.trigger("auth", contents)
        return self.session_id
