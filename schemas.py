from pydantic import BaseModel
from datetime import date
from typing import Optional

class FacultySignupResponse(BaseModel):
    message: str
    pending_faculty_id: str
