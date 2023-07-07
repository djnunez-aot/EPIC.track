# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Exposes all the request validation schemas"""
from .indigenous_nation_request import (
    IndigenousNationBodyParameterSchema, IndigenousNationExistenceQueryParamSchema,
    IndigenousNationIdPathParameterSchema)
from .project_request import ProjectBodyParameterSchema, ProjectExistenceQueryParamSchema, ProjectIdPathParameterSchema
from .proponent_request import (
    ProponentBodyParameterSchema, ProponentExistenceQueryParamSchema, ProponentIdPathParameterSchema)
from .reminder_configuration_request import ReminderConfigurationExistenceQueryParamSchema
from .staff_request import (
    StaffBodyParameterSchema, StaffByPositionsQueryParamSchema, StaffExistanceQueryParamSchema,
    StaffIdPathParameterSchema)
from .task_request import TaskBodyParameterSchema, TaskTemplateBodyParameterSchema, TaskTemplateIdPathParameterSchema
from .type_request import TypeIdPathParameterSchema
from .user_group_request import UserGroupBodyParamSchema, UserGroupPathParamSchema
from .work_request import WorkBodyParameterSchema, WorkExistenceQueryParamSchema, WorkIdPathParameterSchema