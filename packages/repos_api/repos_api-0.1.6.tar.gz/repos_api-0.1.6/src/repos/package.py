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

import json

import appier

class PackageAPI(object):

    def list_packages(self, *args, **kwargs):
        url = self.base_url + "packages"
        contents = self.get(url, auth = False, **kwargs)
        return contents

    def retrieve_package(self, name, version = None, tag = None, extra = None):
        url = self.base_url + "packages/%s" % name
        contents = self.get(
            url,
            version = version,
            tag = tag,
            auth = False,
            redirect = True,
            extra = extra
        )
        return contents

    def publish_package(
        self,
        name,
        version,
        contents = None,
        url = None,
        url_tags = None,
        identifier = None,
        info = None,
        type = None,
        content_type = None
    ):
        _url = self.base_url + "packages"
        contents = contents if isinstance(contents, tuple) or contents == None else\
            appier.FileTuple.from_data(contents)
        info = json.dumps(info)
        if url_tags: url_tags = ["%s:%s" % (tag, url) for tag, url in appier.legacy.iteritems(url_tags)]
        contents = self.post(
            _url,
            data_m = dict(
                name = name,
                version = version,
                contents = contents,
                url = url,
                url_tags = url_tags,
                identifier = identifier,
                info = info,
                type = type,
                content_type = content_type
            )
        )
        return contents

    def info_package(self, name, version = None):
        url = self.base_url + "packages/%s/info" % name
        contents = self.get(url, version = version, auth = False)
        return contents

    def artifacts_package(self, name, *args, **kwargs):
        url = self.base_url + "packages/%s/artifacts" % name
        contents = self.get(url, auth = False, **kwargs)
        return contents
