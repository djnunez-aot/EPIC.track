# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Resource for Responsibility endpoints."""
from http import HTTPStatus

from flask import jsonify
from flask_restx import Namespace, Resource, cors

from reports_api.services import ResponsibilityService
from reports_api.utils import auth, constants, profiletime
from reports_api.utils.caching import AppCache
from reports_api.utils.util import cors_preflight

from reports_api.schemas import response as res

API = Namespace("responsibilities", description="Responsibility")


@cors_preflight("GET")
@API.route("", methods=["GET", "OPTIONS"])
class Responsibilities(Resource):
    """Endpoint resource to return responsibilities"""

    @staticmethod
    @cors.crossdomain(origin="*")
    @auth.require
    @profiletime
    @AppCache.cache.cached(timeout=constants.CACHE_DAY_TIMEOUT, query_string=True)
    def get():
        """Return all responsibilities."""
        responsibilities = ResponsibilityService.find_all()
        return jsonify(res.ResponsibilityResponseSchema(many=True).dump(responsibilities)), HTTPStatus.OK
