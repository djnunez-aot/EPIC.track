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
"""Service to manage Proponent."""
from typing import IO, List

import numpy as np
import pandas as pd

from api.exceptions import ResourceExistsError, ResourceNotFoundError
from api.models import Proponent, db
from api.models.staff import Staff
from api.utils.token_info import TokenInfo


class ProponentService:
    """Service to manage proponent related operations."""

    @classmethod
    def check_existence(cls, name, proponent_id=None):
        """Checks if an proponent exists with given name"""
        return Proponent.check_existence(name, proponent_id)

    @classmethod
    def find_all_proponents(cls):
        """Find all active proponent"""
        proponents = Proponent.find_all(default_filters=False)
        return proponents

    @classmethod
    def find_by_id(cls, proponent_id):
        """Find by indigenous nation id."""
        proponent = Proponent.find_by_id(proponent_id)
        if proponent:
            return proponent
        raise ResourceNotFoundError(f"Proponent with id '{proponent_id}' not found.")

    @classmethod
    def create_proponent(cls, payload: dict):
        """Create a new proponent."""
        exists = cls.check_existence(payload["name"])
        if exists:
            raise ResourceExistsError("Proponent with same name exists")
        proponent = Proponent(**payload)
        proponent.save()
        return proponent

    @classmethod
    def update_proponent(cls, proponent_id: int, payload: dict):
        """Update existing proponent."""
        exists = cls.check_existence(payload["name"], proponent_id)
        if exists:
            raise ResourceExistsError("Proponent with same name exists")
        proponent = Proponent.find_by_id(proponent_id)
        if not proponent:
            raise ResourceNotFoundError(
                f"Proponent with id '{proponent_id}' not found."
            )
        proponent = proponent.update(payload)
        return proponent

    @classmethod
    def delete_proponent(cls, proponent_id: int):
        """Delete proponent by id."""
        proponent = Proponent.find_by_id(proponent_id)
        proponent.is_deleted = True
        proponent.save()
        return True

    @classmethod
    def import_proponents(cls, file: IO):
        """Import proponents"""
        data = cls._read_excel(file)
        data["relationship_holder_id"] = data.apply(
            lambda x: x["relationship_holder_id"].lower()
            if x["relationship_holder_id"]
            else None,
            axis=1,
        )
        relationship_holders = data["relationship_holder_id"].to_list()
        staffs = (
            db.session.query(Staff)
            .filter(Staff.email.in_(relationship_holders), Staff.is_active.is_(True))
            .all()
        )

        data["relationship_holder_id"] = data.apply(
            lambda x: cls._find_staff_id(x["relationship_holder_id"], staffs), axis=1
        )
        username = TokenInfo.get_username()
        data["created_by"] = username
        data = data.to_dict("records")
        db.session.bulk_insert_mappings(Proponent, data)
        db.session.commit()
        return "Created successfully"

    @classmethod
    def _read_excel(cls, file: IO) -> pd.DataFrame:
        """Read the template excel file"""
        column_map = {
            "Name": "name",
            "Relationship Holder": "relationship_holder_id",
        }
        data_frame = pd.read_excel(file)
        data_frame = data_frame.replace({np.nan: None})
        data_frame.rename(column_map, axis="columns", inplace=True)
        return data_frame

    @classmethod
    def _find_staff_id(cls, email: str, staffs: List[Staff]) -> int:
        """Find and return the id of staff from given list"""
        if email is None:
            return None
        staff = next((x for x in staffs if x.email == email), None)
        if staff is None:
            raise ResourceNotFoundError(f"Staff with email {email} does not exist")
        return staff.id
