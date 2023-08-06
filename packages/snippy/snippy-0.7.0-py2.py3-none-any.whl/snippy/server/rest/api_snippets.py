#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution and code snippet management.
#  Copyright 2017-2018 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""api_snippets.py - JSON REST API for Snippets."""

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from snippy.config.source.api import Api
from snippy.content.snippet import Snippet
from snippy.logger import Logger
from snippy.server.rest.jsonapiv1 import JsonApiV1
from snippy.server.rest.validate import Validate


class ApiSnippets(object):
    """Process snippet collections."""

    def __init__(self, storage):
        self._logger = Logger(__name__).logger
        self.storage = storage

    @Logger.timeit
    def on_post(self, request, response):
        """Create new snippets."""

        contents = []
        self._logger.debug('run post /snippy/api/v1/snippets')
        collection = Validate.collection(request.media)
        for member in collection:
            api = Api(Const.SNIPPET, Api.CREATE, member)
            Config.load(api)
            contents.extend(Snippet(self.storage, Const.CONTENT_TYPE_JSON).run())
        if Cause.is_ok():
            response.content_type = Const.MEDIA_JSON_API
            response.body = JsonApiV1.collection(Const.SNIPPET, contents)
            response.status = Cause.http_status()
        else:
            response.content_type = Const.MEDIA_JSON_API
            response.body = JsonApiV1.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end post /snippy/api/v1/snippets')

    @Logger.timeit
    def on_get(self, request, response):
        """Search snippets based on query parameters."""

        self._logger.debug('run get /snippy/api/v1/snippets')
        api = Api(Const.SNIPPET, Api.SEARCH, request.params)
        Config.load(api)
        contents = Snippet(self.storage, Const.CONTENT_TYPE_JSON).run()
        if not contents:
            Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find resources')
        if Cause.is_ok():
            response.content_type = Const.MEDIA_JSON_API
            response.body = JsonApiV1.collection(Const.SNIPPET, contents)
            response.status = Cause.http_status()
        else:
            response.content_type = Const.MEDIA_JSON_API
            response.body = JsonApiV1.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end get /snippy/api/v1/snippets')

    @Logger.timeit
    def on_delete(self, request, response):
        """Delete snippet based on query parameters."""

        self._logger.debug('run delete /snippy/api/v1/snippets')
        api = Api(Const.SNIPPET, Api.DELETE, request.params)
        Config.load(api)
        Snippet(self.storage, Const.CONTENT_TYPE_JSON).run()
        if Cause.is_ok():
            response.status = Cause.http_status()
        else:
            response.content_type = Const.MEDIA_JSON_API
            response.body = JsonApiV1.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end delete /snippy/api/v1/snippets')


class ApiSnippetsDigest(object):
    """Process snippet based on digest resource ID."""

    def __init__(self, storage):
        self._logger = Logger(__name__).logger
        self.storage = storage

    @Logger.timeit
    def on_put(self, request, response, digest):
        """Update snippet based on digest."""

        self._logger.debug('run put /snippy/api/v1/snippets/%s', digest)
        resource_ = Validate.resource(request.media, digest)
        if resource_:
            api = Api(Const.SNIPPET, Api.UPDATE, resource_)
            Config.load(api)
            contents = Snippet(self.storage, Const.CONTENT_TYPE_JSON).run()
        if Cause.is_ok():
            response.content_type = Const.MEDIA_JSON_API
            response.body = JsonApiV1.resource(Const.SNIPPET, contents, request.uri)
            response.status = Cause.http_status()
        else:
            response.content_type = Const.MEDIA_JSON_API
            response.body = JsonApiV1.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end put /snippy/api/v1/snippets/%s', digest)

    @Logger.timeit
    def on_get(self, request, response, digest):
        """Search snippet based on digest."""

        self._logger.debug('run get /snippy/api/v1/snippets/%s', digest)
        local_params = {'digest': digest}
        api = Api(Const.SNIPPET, Api.SEARCH, local_params)
        Config.load(api)
        contents = Snippet(self.storage, Const.CONTENT_TYPE_JSON).run()
        if not contents:
            Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find resource')
        if Cause.is_ok():
            response.content_type = Const.MEDIA_JSON_API
            response.body = JsonApiV1.resource(Const.SNIPPET, contents, request.uri)
            response.status = Cause.http_status()
        else:
            response.content_type = Const.MEDIA_JSON_API
            response.body = JsonApiV1.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end get /snippy/api/v1/snippets/%s', digest)

    @Logger.timeit
    def on_delete(self, _, response, digest):
        """Delete snippet based on digest."""

        self._logger.debug('run delete /snippy/api/v1/snippets/%s', digest)
        local_params = {'digest': digest}
        api = Api(Const.SNIPPET, Api.DELETE, local_params)
        Config.load(api)
        Snippet(self.storage, Const.CONTENT_TYPE_JSON).run()
        if Cause.is_ok():
            response.status = Cause.http_status()
        else:
            response.content_type = Const.MEDIA_JSON_API
            response.body = JsonApiV1.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end delete /snippy/api/v1/snippets/%s', digest)
