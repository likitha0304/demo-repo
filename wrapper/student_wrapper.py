from models import Student

class Studentwrapper:
    @staticmethod
    async def get_student(student_id):
        student=await Student.get(id=student_id)
        return student
    @staticmethod
    async def get_all_students():
        students = await Student.all()
        return students
    @staticmethod
    async def create_student(data):
        student= await Student.create(**data)
        return student
    
    @staticmethod
    async def update_student_details(student_id,data):
        student=await Student.get(id=student_id)
        if student:
            for key,value in data.items():
                setattr(student,key,value)
            await student.save()
        return student
    
    @staticmethod
    async def delete_student(student_id):
        student=await Student.get(id=student_id)
        await student.delete()

