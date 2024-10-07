
from tortoise import  fields
from tortoise.models import Model
from pydantic import BaseModel
from typing import List
class Student(Model):
    id=fields.IntField(pk=True)
    name=fields.CharField(max_length=255)
    grade=fields.IntField()
    roll=fields.IntField()
    email=fields.CharField(max_length=255)
    phone=fields.CharField(max_length=15)
    subjects=fields.JSONField()
    friends=fields.JSONField()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "grade": self.grade,
            "roll": self.roll,
            "email": self.email,
            "phone": self.phone,
            "subjects": self.subjects,
            "friends": self.friends,
        }

    class Meta:
        table="students"

class StudentModel(BaseModel):
    name:str
    grade:int
    roll:int
    email:str
    phone:str
    subjects:List[str]
    friends:List[str]
