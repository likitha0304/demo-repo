from sanic import Sanic
from sanic import response
from sanic.response import json
from pydantic import BaseModel
from pydantic import validator
from sanic.request import Request
#from sanic_ext import Extend
import models
import os
from tortoise import Tortoise
from tortoise.contrib.sanic import register_tortoise
from config import DATABASE_URL,TORTOISE_ORM
from models.students import Student
from wrapper.student_wrapper import Studentwrapper
from sanic_ext import Extend
from sanic_ext import openapi
from tortoise.exceptions import DoesNotExist
app=Sanic(__name__)

Extend(app)





@app.listener('before_server_start')
async def init_db(app, loop):
    await Tortoise.init(
       config=TORTOISE_ORM
    )
    await Tortoise.generate_schemas()

@app.listener('after_server_stop')
async def close_db(app, loop):
    await Tortoise.close_connections()

@app.route('/students', strict_slashes=True)
@openapi.definition(
    summary="This will give the list of students",
    description="This will give the list of all students. Each student object will be a dictionary."
)
@openapi.response(200, content={
    "application/json": {
        "schema": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer"
                    },
                    "name": {
                        "type": "string"
                    },
                    "grade": {
                        "type": "integer"
                    },
                    "roll": {
                        "type": "integer"
                    },
                    "email": {
                        "type": "string"
                    },
                    "phone": {
                        "type": "string"  # Phone numbers are typically strings to handle formats like "+1-123-456-7890"
                    },
                    "subjects": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "friends": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    }
                }
            }
        }
    }
})
@openapi.response(
    status=500,
    content={
        "application/json":{
            "schema":{
                "type":"object",
                "properties":{
                    "message":{
                        "type":"string",
                        "example":"internal server problem"
                    }
                }
            }
        }
    }
)
async def get_students(request):
    try:
        students=await Studentwrapper.get_all_students()
        return json([
            student.to_dict()
             for student in students])
    except Exception as e:
        return response.json({"message":str(e)},status=500)


@app.route("/students/<student_id:int>")
@openapi.definition(
    summary="this will give the student earing student is",
    description="this will the student with stduent id ,it will only return a single student as id is unique"
)
@openapi.parameter(
    name="student_id",
    location="path",
    required=True,
    schema={
        "type":"integer"
    },
    descrption="this is the id of the student which u wanted to retrive"
)
@openapi.response(
    status=200,
    content={
        "application/json":{
            "schema":{
                "type":"object",
                "properties":{
                     "id": {
                        "type": "integer"
                    },
                    "name": {
                        "type": "string"
                    },
                    "grade": {
                        "type": "integer"
                    },
                    "roll": {
                        "type": "integer"
                    },
                    "email": {
                        "type": "string"
                    },
                    "phone": {
                        "type": "string"  # Phone numbers are typically strings to handle formats like "+1-123-456-7890"
                    },
                    "subjects": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "friends": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    }

                }
            }
        }
    }
)
@openapi.response(
   status=404,
   content={
        "application/json":{
            "schema":{
                "type":"object",
                "properties":{
                    "description":{
                        "type":"string"
                    },
                    "status":{
                        "type":"integer",
                        "example": 404
                    },
                    "message":{
                        "type":"string"
                    }
                }
            }
        }
    }
    
)
@openapi.response(
    status=500,
    content={
        "application/json":{
            "schema":{
                "type":"object",
                "properties":{
                    "message":{
                        "type":"string",
                        "example":"internal server problem"
                    }
                }
            }
        }
    }
)

async def get_student_by_id(request, student_id):
    try:
        student = await Studentwrapper.get_student(student_id)  # This returns a single Student instance
        return response.json(student.to_dict())  # Convert the single student to a dict
    except DoesNotExist:
        return response.json({"error": "Student not found"}, status=404)  # Return a 404 if not found
    except Exception as e:
        return response.json({"message":str(e)},status=500)


@app.post("/")
@openapi.definition(
    summary="new student will be stored",
    description="this will ccreate a new entry in the database table",
    
)
@openapi.parameter(
    "student",
    "body",
    {
        "type": "object",
        "properties": {
            "id": {
                "type": "integer"
                },
            "name": {
                "type": "string"
                },
            "grade": {
                "type": "integer"
                },
            "roll": {
                "type": "integer"
                },
            "email": {
                "type": "string"
                },
            "phone": {
                "type": "string"
                },
            "subjects": {
                "type": "array",
                "items": {"type": "string"},
            },
            "friends": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
        "required": ["name", "grade", "roll", "email", "phone","subjects"],  # Optional: Specify required fields
    },
    required=True,
)

@openapi.response(
    status=200,
    content={
        "application/json":{
            "schema":{
                "type":"object",
                "properties":{
                     "id": {
                        "type": "integer"
                    },
                    "name": {
                        "type": "string"
                    },
                    "grade": {
                        "type": "integer"
                    },
                    "roll": {
                        "type": "integer"
                    },
                    "email": {
                        "type": "string"
                    },
                    "phone": {
                        "type": "string"  # Phone numbers are typically strings to handle formats like "+1-123-456-7890"
                    },
                    "subjects": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "friends": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    }

                }
            }
        }
    }
)
@openapi.response(
   status=404,
   content={
        "application/json":{
            "schema":{
                "type":"object",
                "properties":{
                    "description":{
                        "type":"string"
                    },
                    "status":{
                        "type":"integer",
                        "example": 404
                    },
                    "message":{
                        "type":"string",
                        "example":"student cannot be created"
                    }
                }
            }
        }
    }
    
)
@openapi.response(
    status=500,
    content={
        "application/json":{
            "schema":{
                "type":"object",
                "properties":{
                    "message":{
                        "type":"string",
                        "example":"internal server problem"
                    }
                }
            }
        }
    }
)
async def new_student(request):
    data=request.json
    try:
        student= await Studentwrapper.create_student(data)
        return response.json(student.to_dict())
    except Exception as e:
        return response.json({"message":str(e)},status=500)


@app.put("/students/<student_id:int>")
@openapi.definition(
    summary="student who is already present will be updated",
    description="this will update the current student details all columns will be updated",
    
)
@openapi.parameter(
    name="student_id",
    location="path",
    description="The ID of the student to update",
    required=True,
    schema={"type": "integer"}
)
@openapi.parameter(
    "student",
    "body",
    {
        "type": "object",
        "properties": {
            "id": {
                "type": "integer"
                },
            "name": {
                "type": "string"
                },
            "grade": {
                "type": "integer"
                },
            "roll": {
                "type": "integer"
                },
            "email": {
                "type": "string"
                },
            "phone": {
                "type": "string"
                },
            "subjects": {
                "type": "array",
                "items": {"type": "string"},
            },
            "friends": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
        "required": ["name", "grade", "roll", "email", "phone","subjects"],  # Optional: Specify required fields
    },
    required=True,
)
@openapi.response(
    status=200,
    content={
        "application/json":{
            "schema":{
                "type":"object",
                "properties":{
                     "id": {
                        "type": "integer"
                    },
                    "name": {
                        "type": "string"
                    },
                    "grade": {
                        "type": "integer"
                    },
                    "roll": {
                        "type": "integer"
                    },
                    "email": {
                        "type": "string"
                    },
                    "phone": {
                        "type": "string"  # Phone numbers are typically strings to handle formats like "+1-123-456-7890"
                    },
                    "subjects": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "friends": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    }

                }
            }
        }
    }
)
@openapi.response(
   status=400,
   content={
        "application/json":{
            "schema":{
                "type":"object",
                "properties":{
                    
                    "message":{
                        "type":"string",
                        "example":"student not found"
                    }
                }
            }
        }
    }
    
)
@openapi.response(
    status=500,
    content={
        "application/json":{
            "schema":{
                "type":"object",
                "properties":{
                    "message":{
                        "type":"string",
                        "example":"internal server problem"
                    }
                }
            }
        }
    }
)
async def update_student_entry(request, student_id):
    body = request.json  # Get the request body
    try:
         student = await Studentwrapper.update_student_details(student_id,body)  
         if student:
            return response.json(student.to_dict())
    except DoesNotExist:
        return response.json({"message":"student not found"},status=400)
    except Exception as e:
        return response.json({"message":str(e)},status=500)

@app.delete("/students/<student_id:int>")
@openapi.definition(
    summary="student who is already present will be deleted",
    description="this will delete the current student details all columns will be deleted",
    
)
@openapi.parameter(
    name="student_id",
    location="path",
    description="The ID of the student to update",
    required=True,
    schema={"type": "integer"}
)
@openapi.response(
   status=200,
   content={
        "application/json":{
            "schema":{
                "type":"object",
                "properties":{
                    
                    "message":{
                        "type":"string",
                        "example":"student not found"
                    }
                }
            }
        }
    }
    
)
@openapi.response(
   status=404,
   content={
        "application/json":{
            "schema":{
                "type":"object",
                "properties":{
                    
                    "message":{
                        "type":"string",
                        "example":"student not found"
                    }
                }
            }
        }
    }
    
)
@openapi.response(
   status=500,
   content={
        "application/json":{
            "schema":{
                "type":"object",
                "properties":{
                    
                    "message":{
                        "type":"string",
                        "example":"internal server issue"
                    }
                }
            }
        }
    }
    
)
async def delete_student(request, student_id):
    # Fetch the student by ID
    try:
        student = await Studentwrapper.get_student(student_id)  # Fetch the student with the given ID

        if student:  # Check if the student exists
            await Studentwrapper.delete_student(student_id)  # Delete the student
            return response.json({"message": "student has been successfully deleted"})  # Return success message
    except DoesNotExist:
        return response.json({"message": "student not found"}, status=404)  # Return 404 if not found
    except Exception as e:
        return response.json({"message":str(e)},status=500)



if __name__ =="__main__":
    app.run(host="0.0.0.0",port=8000,debug=True,auto_reload=True)



