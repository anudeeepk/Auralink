from django.db import models

# Create your models here.

class login_table(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    type=models.CharField(max_length=100)

class department_table(models.Model):
    deptname=models.CharField(max_length=100)

class hod_table(models.Model):
    name=models.CharField(max_length=100)
    DEPARTMENT=models.ForeignKey(department_table,on_delete=models.CASCADE)
    LOGIN=models.ForeignKey(login_table,on_delete=models.CASCADE)
    phone=models.BigIntegerField()
    email=models.CharField(max_length=50)
    qualification=models.CharField(max_length=50)
    place=models.CharField(max_length=50)
    post=models.CharField(max_length=50)
    pin=models.BigIntegerField()
    image=models.FileField()

class course_table(models.Model):
    coursename=models.CharField(max_length=100)
    DEPARTMENT = models.ForeignKey(department_table, on_delete=models.CASCADE)
    duration=models.BigIntegerField()

class student_table(models.Model):
    name=models.CharField(max_length=100)
    registerno=models.CharField(max_length=50)
    COURSE=models.ForeignKey(course_table,on_delete=models.CASCADE)
    LOGIN=models.ForeignKey(login_table,on_delete=models.CASCADE)
    semester=models.CharField(max_length=50)
    phone=models.BigIntegerField()
    email=models.CharField(max_length=50)
    image=models.FileField()

class subject_table(models.Model):
    subname=models.CharField(max_length=50)
    COURSE=models.ForeignKey(course_table, on_delete=models.CASCADE)
    semester = models.CharField(max_length=50)

class staff_table(models.Model):
    name = models.CharField(max_length=100)
    DEPARTMENT = models.ForeignKey(department_table, on_delete=models.CASCADE)
    LOGIN = models.ForeignKey(login_table, on_delete=models.CASCADE)
    phone = models.BigIntegerField()
    email = models.CharField(max_length=50)
    image = models.FileField()

class examcell_table(models.Model):
    LOGIN = models.ForeignKey(login_table, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    email = models.CharField(max_length=50)

class examtimetable_table(models.Model):
    examname = models.CharField(max_length=100)
    date=models.DateField()
    semester = models.CharField(max_length=50)
    startingdate=models.DateField()
    status=models.CharField(max_length=20)

class examdetails_table(models.Model):
    EXAM=models.ForeignKey(examtimetable_table,on_delete=models.CASCADE)
    SUBJECT=models.ForeignKey(subject_table,on_delete=models.CASCADE)
    date=models.DateField()
    time=models.TimeField()

class hall_table(models.Model):
    hallnumber=models.CharField(max_length=50)
    details=models.CharField(max_length=200)
    numberofseats=models.BigIntegerField()

class hallallocation_table(models.Model):
    STAFF=models.ForeignKey(staff_table, on_delete=models.CASCADE)
    HALL=models.ForeignKey(hall_table, on_delete=models.CASCADE)
    EXAMDETAILS=models.ForeignKey(examdetails_table, on_delete=models.CASCADE)

class seatingarrangement_table(models.Model):
    STUDENT = models.ForeignKey(student_table, on_delete=models.CASCADE)
    HALL=models.ForeignKey(hall_table, on_delete=models.CASCADE)
    seatingno=models.BigIntegerField()
    TIMETABLE=models.ForeignKey(examtimetable_table, on_delete=models.CASCADE)
    # EXAMDETAILS = models.ForeignKey(examdetails_table, on_delete=models.CASCADE)


class alumni_table(models.Model):
    LOGIN = models.ForeignKey(login_table, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    DEPARTMENT = models.ForeignKey(department_table, on_delete=models.CASCADE)
    phone = models.BigIntegerField()
    email = models.CharField(max_length=50)

class jobdetails_table(models.Model):
    ALUMNI=models.ForeignKey(alumni_table, on_delete=models.CASCADE)
    jobfile=models.FileField()
    jobdescription=models.CharField(max_length=500)
    posteddate=models.DateField()
    experience=models.CharField(max_length=100)

class chat_table(models.Model):
    FROM=models.ForeignKey(login_table, on_delete=models.CASCADE,related_name="fn")
    TO=models.ForeignKey(login_table, on_delete=models.CASCADE,related_name="to")
    msg=models.CharField(max_length=500)
    date=models.DateField()




