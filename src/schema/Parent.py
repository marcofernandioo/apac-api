from pydantic import BaseModel
from typing import List, Union
from .Programme import ProgrammeRead
from .Course import CourseRead


class AssignableResponse(BaseModel):
    items: List[Union[CourseRead, ProgrammeRead]]