from pydantic import BaseModel, Field, validator, root_validator
from typing import Optional
from datetime import datetime
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

class Record(BaseModel):
    id: int = Field(None, title="The ID of the record", example=1)
    intake_fk: str = Field("nah", example="3F2311_1")
    name: str = Field(..., title="The name of the record", max_length=255, example="John Doe")
    start_date: str = Field(None, title="Start Date", example = "2023-06-16T00:00:00Z")
    end_date: str = Field(None, title="End Date", example = "2023-10-16T00:00:00Z")
    duration: Optional[int] = Field(None, title="Duration in weeks")
    # description: Optional[str] = Field(None, title="The description of the record", max_length=1024, example="A brief description")
    # created_at: datetime = Field(default_factory=datetime.utcnow, title="The creation timestamp of the record", example="2023-06-16T00:00:00Z")

    # Uncomment the following line if the duration should be autocalculated.
    # @validator('duration', always=True)
    def calculate_duration(cls, v, values):
        start = values.get('start_date')
        end = values.get('end_date')
        
        if start and end:
            start_date = parse(start)
            end_date = parse(end)
            
            # Calculate the difference
            diff = relativedelta(end_date, start_date)
            
            # Convert to weeks
            weeks = diff.years * 52 + diff.months * 4.34524 + diff.days / 7
            
            # Round to the nearest decimal
            return round(weeks)
        return None

    class Config:
        orm_mode: True
