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
"""Resource for Insight endpoints."""
from http import HTTPStatus

from flask import jsonify, request
from flask_restx import Namespace, Resource, cors

from api.schemas import request as req
from api.schemas import response as res
from api.services.insights import InsightService
from api.utils import auth, constants, profiletime
from api.utils.caching import AppCache
from api.utils.util import cors_preflight
from api.utils.str import natural_sort

API = Namespace("insights", description="Insights")


@cors_preflight("GET")
@API.route("/works", methods=["GET", "OPTIONS"])
class Works(Resource):
    """Endpoint resource to return work insights"""

    @staticmethod
    @cors.crossdomain(origin="*")
    @auth.require
    @profiletime
    @AppCache.cache.cached(timeout=constants.CACHE_DAY_TIMEOUT, query_string=True)
    def get():
        """Return work insights based on group by param."""
        args = req.WorkInsightRequestQueryParameterSchema().load(request.args)
        work_insights = InsightService.fetch_work_insights(args["group_by"])
        response = res.WorkInsightResponseSchema(many=True).dump(work_insights)
        if(args["group_by"] == "lead"):
            response = natural_sort(response, "work_lead")
        if(args["group_by"] == "staff"):
            response = natural_sort(response, "staff")
        if(args["group_by"] == "first_nation"):
            response = natural_sort(response, "first_nation")
        if(args["group_by"] == "team"):
            response = natural_sort(response, "eao_team")
        if(args['group_by' == 'federal_involvement']):
            response = natural_sort(response, 'federal_involvement')
        if(args['group_by' == 'ministry']):
            response = natural_sort(response, 'ministry')
        
        return (
            jsonify(work_insights),
            HTTPStatus.OK,
        )


@cors_preflight("GET")
@API.route("/works/assessment", methods=["GET", "OPTIONS"])
class AssessmentWorks(Resource):
    """Endpoint resource to return assessment works insights"""

    @staticmethod
    @cors.crossdomain(origin="*")
    @auth.require
    @profiletime
    @AppCache.cache.cached(timeout=constants.CACHE_DAY_TIMEOUT, query_string=True)
    def get():
        """Return work insights based on group by param."""
        args = req.WorkInsightRequestQueryParameterSchema().load(request.args)
        work_insights = InsightService.fetch_assessment_work_insights(args["group_by"])
        return jsonify(work_insights), HTTPStatus.OK


@cors_preflight("GET")
@API.route("/projects", methods=["GET", "OPTIONS"])
class Projects(Resource):
    """Endpoint resource to return project insights"""

    @staticmethod
    @cors.crossdomain(origin="*")
    @auth.require
    @profiletime
    @AppCache.cache.cached(timeout=constants.CACHE_DAY_TIMEOUT, query_string=True)
    def get():
        """Return project insights based on group by param."""
        args = req.ProjectInsightRequestQueryParameterSchema().load(request.args)
        project_insights = InsightService.fetch_project_insights(args["group_by"], args["type_id"])
        return jsonify(project_insights), HTTPStatus.OK
