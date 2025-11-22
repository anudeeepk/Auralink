import json
import random

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from myapp.models import *
from django.http import HttpResponse, JsonResponse
from datetime import date, datetime


# Create your views here.
def login(request):
    return render(request,'index.html')


def login_post(request):
    username=request.POST['textfield']
    password=request.POST['textfield2']

    ob=login_table.objects.filter(username=username,password=password)
    if ob.exists():
        obb = login_table.objects.get(username=username, password=password)
        if obb.type == 'admin':
            request.session['lid']=obb.id
            return HttpResponse('''<script>alert('admin login successfull');window.location='/admin_home'</script>''')
        elif obb.type == 'examcell':
            request.session['lid'] = obb.id
            return HttpResponse('''<script>alert('examcell login successfull');window.location='/Examcell_home'</script>''')
        elif obb.type == 'hod':
            request.session['lid'] = obb.id
            return HttpResponse(
                '''<script>alert('Hod login successfull');window.location='/hod_home'</script>''')


        else:
            return HttpResponse('''<script>alert('invalid');window.location='/'</script>''')
    else:
        return HttpResponse('''<script>alert('invalid');window.location='/'</script>''')


def admin_home(request):
    return render(request,'Admin/index.html')

def add_course(request):
    ob=department_table.objects.all()
    return render(request, 'Admin/Add Course.html',{'val':ob})

def add_course_post(request):
    coursename = request.POST['textfield']
    department = request.POST['textfield2']
    duration = request.POST['textfield3']

    obd = department_table()
    obd.deptname = department
    obd.save()

    obc=course_table()
    obc.coursename=coursename
    obc.DEPARTMENT=department_table.objects.get(id=department)
    obc.duration=duration
    obc.save()
    return HttpResponse('''<script>alert('inserted');window.location='/view_Course'</script>''')


def add_Examcell(request):
    return render(request, 'Admin/Add Exam cell.html')

def add_Examcell_post(request):
    name=request.POST['textfield']
    phone=request.POST['textfield2']
    email=request.POST['textfield3']
    username=request.POST['textfield4']
    password=request.POST['textfield5']

    ob=login_table()
    ob.username=username
    ob.password=password
    ob.type='examcell'
    ob.save()

    obe=examcell_table()
    obe.LOGIN = ob
    obe.name =name
    obe.phone = phone
    obe.email =email
    obe.save()
    return HttpResponse('''<script>alert('inserted');window.location='/view_Examcell'</script>''')


def add_Hod(request):
    ob = department_table.objects.all()
    return render(request, 'Admin/Add Hod.html',{"val":ob})

def add_hod_post(request):
    username = request.POST['textfield4']
    password = request.POST['textfield5']
    name=request.POST['textfield10']
    department = request.POST['select']
    phone = request.POST['textfield3']
    email = request.POST['textfield4']
    qualification = request.POST['textfield5']
    place = request.POST['textfield6']
    post = request.POST['textfield7']
    pin = request.POST['textfield8']
    image = request.FILES['textfield9']

    fs=FileSystemStorage()
    fp=fs.save(image.name,image)

    ob = login_table()
    ob.username =username
    ob.password =password
    ob.type = 'hod'
    ob.save()

    obh = hod_table()
    obh.LOGIN = ob
    obh.name = name
    obh.DEPARTMENT=department_table.objects.get(id=department)
    obh.phone = phone
    obh.email = email
    obh.qualification=qualification
    obh.place=place
    obh.post=post
    obh.pin=pin
    obh.image=fp
    obh.save()

    return HttpResponse('''<script>alert('inserted');window.location='/view_Hod'</script>''')

    return render(request, 'Admin/View HoD.html')


def add_Subject(request):
    ob=course_table.objects.all()
    return render(request, 'Admin/Add Subject.html',{'val':ob})

def add_subject_post(request):
    subname = request.POST['textfield']
    course = request.POST['textfield2']
    semester = request.POST['select']

    obs=subject_table()
    obs.subname=subname
    obs.COURSE=course_table.objects.get(id=course)
    obs.semester=semester
    obs.save()

    return HttpResponse('''<script>alert('inserted');window.location='/view_Subject'</script>''')



def view_Course(request):
    ob = course_table.objects.all()
    return render(request, 'Admin/View Course.html',{'val':ob})

def delete_course(request,id):
    ob=course_table.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert('Deleted Successfully');window.location='/view_Course'</script>''')

def edit_course(request,id):
    request.session['cid']=id
    ob1 = department_table.objects.all()
    ob=course_table.objects.get(id=id)
    return render(request,"Admin/Edit Course.html",{"data":ob,"val":ob1})

def edit_course_post(request):
    coursename = request.POST['textfield']
    department = request.POST['department']
    duration = request.POST['duration']


    obec=course_table.objects.get(id=request.session['cid'])
    obec.coursename=coursename
    obec.DEPARTMENT=department_table.objects.get(id=department)
    obec.duration =duration
    obec.save()
    return HttpResponse('''<script>alert('Successfully Edited');window.location='/view_Course'</script>''')

def view_Examcell(request):
    ob=examcell_table.objects.all()
    return render(request, 'Admin/View Exam Cell.html',{'val':ob})


def delete_examcell(request,id):
    ob=login_table.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert('Deleted Successfully');window.location='/view_Examcell'</script>''')


def edit_examcell(request,id):
    request.session['eid']=id
    ob=examcell_table.objects.get(id=id)
    return render(request,"Admin/Edit Exam cell.html",{"data":ob})

def edit_examcell_post(request):
    name = request.POST['name']
    phone = request.POST['phone']
    email = request.POST['email']

    obee=examcell_table.objects.get(id=request.session['eid'])
    obee.name=name
    obee.phone=phone
    obee.email =email
    obee.save()
    return HttpResponse('''<script>alert('Successfully Edited');window.location='/view_Examcell'</script>''')

def view_Hod(request):
    ob = hod_table.objects.all()
    return render(request, 'Admin/View HoD.html',{'val':ob})

def delete_hod(request,id):
    ob=login_table.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert('Deleted Successfully');window.location='/view_Hod'</script>''')

def edit_hod(request,id):
    request.session['hid']=id
    ob=hod_table.objects.get(id=id)
    a=department_table.objects.all()
    return render(request,"Admin/Edit Hod.html",{"data":ob,"data1":a})

def edit_hod_post(request):
    name = request.POST['name']
    department = request.POST['select']
    phone = request.POST['phone']
    email = request.POST['email']
    qualification = request.POST['qualification']
    place = request.POST['place']
    post = request.POST['post']
    pin = request.POST['pin']
    image = request.FILES['image']

    fs = FileSystemStorage()
    fp = fs.save(image.name, image)

    obd = department_table()
    obd.deptname = department
    obd.save()

    obh = hod_table.objects.get(id=request.session['hid'])
    obh.name = name
    obh.DEPARTMENT = obd
    obh.phone = phone
    obh.email = email
    obh.qualification = qualification
    obh.place = place
    obh.post = post
    obh.pin = pin
    obh.image = fp
    obh.save()
    return HttpResponse('''<script>alert('Successfully Edited');window.location='/view_Hod'</script>''')

def view_student(request):
    ob = student_table.objects.all()
    return render(request,'Admin/View Student.html',{'val':ob})

def view_Subject(request):
    ob = subject_table.objects.all()
    return render(request, 'Admin/View Subject.html',{'val':ob})

def delete_subject(request,id):
    ob=subject_table.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert('Deleted Successfully');window.location='/view_Subject'</script>''')

def edit_subject(request,id):
    request.session['sid']=id
    ob2 = course_table.objects.all()
    ob=subject_table.objects.get(id=id)
    return render(request,"Admin/Edit Subject.html",{"data":ob,"val":ob2 })

def edit_subject_post(request):
    subname = request.POST['subname']
    course = request.POST['course']
    semester = request.POST['select']

    obes=subject_table.objects.get(id=request.session['sid'])
    obes.subname=subname
    obes.COURSE_id=course
    obes.semester =semester
    obes.save()
    return HttpResponse('''<script>alert('Successfully Edited');window.location='/view_Subject'</script>''')



def add_examdetails(request):
    ob=subject_table.objects.filter(semester=request.session["sem"])
    return render(request, 'Exam Cell/Add Exam Details.html',{"subjects":ob})

def add_examdetails_post(request):
    course=request.POST['select']
    date = request.POST['date']
    time = request.POST['time']
    subname = request.POST['select1']

    obs = examdetails_table()
    obs.EXAM_id = request.session["examid"]
    obs.SUBJECT = subject_table.objects.get(id=subname)
    obs.SUBJECT = subject_table.objects.get(id=course)
    obs.date = date
    obs.time = time
    obs.save()

    return HttpResponse('''<script>alert('inserted');window.location='/view_examtimetable'</script>''')


def view_examdetails(request,id):
    ob=examtimetable_table.objects.get(id=id)
    request.session["examid"]=id
    request.session["sem"]=ob.semester

    bb=examdetails_table.objects.all()
    return render(request,'Exam Cell/View Exam Details.html',{'data':bb})

def delete_examdetails(request,id):
    ob=examdetails_table.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert('Deleted Successfully');window.location='/examcell_home'</script>''')

def edit_examdetails(request,id):
    request.session['eid']=id
    ob=examdetails_table.objects.get(id=id)
    return render(request,"Admin/Edit Exam Details.html",{"data":ob})

def edit_examdetails_post(request):
    course = request.POST['select']
    date = request.POST['date']
    time = request.POST['time']
    subname = request.POST['select1']

    obs = examdetails_table()
    obs.EXAM_id = request.session["examid"]
    obs.SUBJECT = subject_table.objects.get(id=subname)
    obs.SUBJECT = subject_table.objects.get(id=course)
    obs.date = date
    obs.time = time
    obs.save()

    return HttpResponse('''<script>alert('inserted');window.location='/view_examdetails'</script>''')

def add_Examhall(request):
    ob=hall_table.objects.all()
    return render(request,'Exam Cell/Add Exam Hall.html',{"hall":ob})

def add_Examhall_post(request):
    hallnumber=request.POST['textfield']
    details=request.POST['textfield2']
    numberofseats=request.POST['textfield3']

    obe=hall_table()
    obe.hallnumber =hallnumber
    obe.details = details
    obe.numberofseats =numberofseats
    obe.save()
    return HttpResponse('''<script>alert('inserted');window.location='/view_examhall'</script>''')


def add_Examtimetable(request):
    return render(request,'Exam Cell/Add Exam Timetable.html')

def add_Examtimetable_post(request):
    examname=request.POST['textfield']
    # date=request.POST['textfield2']
    semester=request.POST['select']
    startingdate=request.POST['textfield2']
    status=request.POST['textfield5']

    obe=examtimetable_table()
    obe.examname = examname

    obe.date =date.today()
    obe.semester = semester
    obe.startingdate =startingdate
    obe.status = status
    obe.save()
    return HttpResponse('''<script>alert('inserted');window.location='/view_examtimetable'</script>''')


def Examcell_home(request):
    return render(request,'Exam Cell/index.html')

def view_examhall(request):
    ob = hall_table.objects.all()
    return render(request,'Exam Cell/View Exam Hall.html',{'val':ob})

def delete_examhall(request,id):
    ob=hall_table.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert('Deleted Successfully');window.location='/view_examhall'</script>''')


def edit_examhall(request,id):
    request.session['eid']=id
    ob=hall_table.objects.get(id=id)
    return render(request,"Exam Cell/Edit Exam Hall.html",{"data":ob})

def edit_examhall_post(request):
    hallnumber = request.POST['textfield']
    details = request.POST['textfield2']
    numberofseats = request.POST['textfield3']

    obee=hall_table.objects.get(id=request.session['eid'])
    obee.hallnumber=hallnumber
    obee.details=details
    obee.numberofseats =numberofseats
    obee.save()
    return HttpResponse('''<script>alert('Successfully Edited');window.location='/view_examhall'</script>''')

def view_examtimetable(request):
    ob = examtimetable_table.objects.all()
    return render(request,'Exam Cell/View Exam Timetable.html',{'val':ob})

def delete_examtimetable(request,id):
    ob=examtimetable_table.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert('Deleted Successfully');window.location='/view_examtimetable'</script>''')


def edit_examtimetable(request,id):
    request.session['eid']=id
    ob=examtimetable_table.objects.get(id=id)
    return render(request,"Exam Cell/Edit Exam Timetable.html",{"data":ob,"d":str(ob.startingdate)})

def edit_examtimetable_post(request):
    examname = request.POST['textfield']
    semester = request.POST['select']
    startingdate = request.POST['textfield2']
    status = request.POST['textfield5']

    obee=examtimetable_table.objects.get(id=request.session['eid'])
    obee.examname=examname
    obee.semester=semester
    obee.startingdate =startingdate
    obee.status =status
    obee.save()
    return HttpResponse('''<script>alert('Successfully Edited');window.location='/view_examtimetable'</script>''')

def view_seatingalloc(request):
    if request.method=='POST':
        xm=request.POST['select']


    ob = examtimetable_table.objects.all()
    return render(request,'Exam Cell/View Seating Alloc.html',{"val":ob})

def view_examdate(request):
    return render(request,'Exam Cell/View date.html')

def hod_home(request):
    return render(request,'HoD/index.html')


def add_hodstudent(request):
    ob=course_table.objects.all()
    return render(request,'HoD/Add Hod Student.html',{"val":ob})

def add_hodstudent_post(request):
    name=request.POST['textfield']
    registerno=request.POST['textfield2']
    course=request.POST['select']
    semester=request.POST['select2']
    phone=request.POST['textfield3']
    email = request.POST['textfield4']
    image = request.FILES['file']

    fs = FileSystemStorage()
    fp = fs.save(image.name, image)

    ob=login_table()
    ob.username=email
    ob.password=phone
    ob.type='student'
    ob.save()

    obes=student_table()
    obes.LOGIN = ob
    obes.name = name
    obes.COURSE = course_table.objects.get(id=course)
    obes.registerno = registerno
    obes.semester = semester
    obes.phone = phone
    obes.email = email
    obes.image = fp
    obes.save()
    return HttpResponse('''<script>alert('inserted');window.location='/view_hodstudent'</script>''')

def view_hodstudent(request):
    ob = student_table.objects.all()
    return render(request,'HoD/View Hod Student.html',{'val':ob})

def edit_hodstudent(request,id):
    request.session['eid']=id
    ob=student_table.objects.get(id=id)
    ob1=course_table.objects.all()
    return render(request,"HoD/Edit Hod Student.html",{"data":ob,"val":ob1})

def edit_hodstudent_post(request):
    name = request.POST['textfield']
    registerno = request.POST['textfield2']
    course = request.POST['select']
    semester = request.POST['select2']
    phone = request.POST['textfield3']
    email = request.POST['textfield4']
    image = request.FILES['file']

    fs = FileSystemStorage()
    fp = fs.save(image.name, image)

    obes = student_table.objects.get(id=request.session['eid'])
    obes.name = name
    obes.COURSE = course_table.objects.get(id=course)
    obes.registerno = registerno
    obes.semester = semester
    obes.phone = phone
    obes.email = email
    obes.image = fp
    obes.save()
    return HttpResponse('''<script>alert('Successfully Edited');window.location='/view_hodstudent'</script>''')


def delete_hodstudent(request,id):
    ob=student_table.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert('Deleted Successfully');window.location='/view_hodstudent'</script>''')


def add_hodstaff(request):
    ob = hod_table.objects.filter(LOGIN__id=request.session['lid'])
    obb = department_table.objects.all()
    print(ob,"jjj")
    return render(request,'HoD/Add Hod Staff.html',{'val':ob,'value':obb})

def add_hodstaff_post(request):
    name = request.POST['textfield']
    department = request.POST['select']
    phone = request.POST['textfield2']
    email = request.POST['textfield22']
    image = request.FILES['file']

    fs = FileSystemStorage()
    fp = fs.save(image.name, image)

    obes = staff_table()
    obes.name = name
    obes.DEPARTMENT_id =department
    obes.phone = phone
    obes.email = email
    obes.image = fp
    obes.save()
    return HttpResponse('''<script>alert('inserted');window.location='/view_staff'</script>''')


def view_staff(request):
    ob = staff_table.objects.all()
    return render(request,'HoD/View Hod Staff.html',{'val':ob})

def edit_staff(request,id):
    request.session['eid']=id
    ob=staff_table.objects.get(id=id)
    obb = department_table.objects.all()
    ob1 = hod_table.objects.filter(LOGIN__id=request.session['lid'])
    return render(request,"HoD/Edit Hod Staff.html",{"data":ob,"val":ob1,"value":obb})


def edit_hodstaff_post(request):
    name = request.POST['textfield']
    department = request.POST['select']
    phone = request.POST['textfield2']
    email = request.POST['textfield22']
    image = request.FILES['file']

    fs = FileSystemStorage()
    fp = fs.save(image.name, image)

    obes = staff_table.objects.get(id=request.session['eid'])
    obes.name = name

    obes.phone = phone
    obes.DEPARTMENT_id = department
    obes.email = email
    obes.image = fp
    obes.save()
    return HttpResponse('''<script>alert('Successfully Edited');window.location='/view_staff'</script>''')

def delete_hodstaff(request,id):
    ob=staff_table.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert('Deleted Successfully');window.location='/view_staff'</script>''')


def add_examduty(request):
    ob = hall_table.objects.all()
    ob1 = examdetails_table.objects.all()
    return render(request,'HoD/Add Hod Hallalloc.html',{'val':ob,"data":ob1})

def add_examduty_post(request):
    hall=request.POST['select']
    examdetails=request.POST['select1']
    kk=request.session['sfid']
    obes=hallallocation_table()
    obes.STAFF = staff_table.objects.get(id=request.session['sfid'])
    obes.HALL = hall_table.objects.get(id=hall)
    obes.EXAMDETAILS = examdetails_table.objects.get(id=examdetails)
    obes.save()
    return HttpResponse(f'''<script>alert('inserted');window.location='/view_examduty/{kk}'</script>''')

def view_examduty(request,id):
    request.session['sfid']=id
    ob = hallallocation_table.objects.filter(STAFF__id=request.session['sfid'])
    return render(request,'HoD/View Hod Hallalloc.html',{'val':ob})

def add_hallarrangement(request):
    ob=seatingarrangement_table.objects.all()
    ob1=hall_table.objects.all()
    return render(request,'HoD/Add Hod Seating.html',{'val':ob,"data":ob1})

def add_hallarrangement_post(request):
    examdetails=request.POST['textfield']
    student=request.POST['textfield2']
    hall=request.POST['select']
    seatingno=request.POST['textfield3']

    obes=seatingarrangement_table()
    obes.STUDENT = student_table.objects.get(id=student)
    obes.HALL = hall_table.objects.get(id=hall)
    obes.seatingno = seatingno
    obes.save()
    return HttpResponse('''<script>alert('inserted');window.location='/view_staff'</script>''')


def view_hallarrangement(request):
    ob = seatingarrangement_table.objects.all()
    return render(request, 'HoD/View Hod Seating.html', {"val":ob})

# def add_jobdetails(request):
#     ob = jobdetails_table.objects.all()
#     return render(request,'HoD/Add Hod Jobdetails.html',{"val":ob})

def add_jobdetails_post(request):
    jobfile=request.POST['file']
    jobdescription=request.POST['textfield']
    posteddate=request.POST['textfield2']
    experience = request.POST['textfield3']

    obe=jobdetails_table()
    obe.jobfile =jobfile
    obe.jobdescription = jobdescription
    obe.posteddate = posteddate
    obe.experience =experience
    obe.save()
    return HttpResponse('''<script>alert('inserted');window.location='/view_jobdetails'</script>''')


def view_jobdetails(request):
    ob =jobdetails_table.objects.all()
    return render(request,'HoD/View Hod Jobdetails.html',{"val":ob})

def delete_jobdetails(request,id):
    ob=jobdetails_table.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert('Deleted Successfully');window.location='/view_jobdetails'</script>''')


# def generate_hall(request):
#     exmid = request.form["select"];
#     date = request.form["sel2"];
#     request.session["date"] = date;
#     request.session["exid"] = exmid;
#     s=seatingarrangement_table.objects.filter(EXAMDETAILS__id=exmid,EXAMDETAILS__date=date)
#     if s is not None:
#         return "already"
#     else:
#         ad = list()
#         count = list()
#         course = list()
#         sem = list()
#         time = list()
#         obexamdet=examdetails_table.objects.filter(id=exmid,date=date)
#         dissub=[]
#         for i in obexamdet:
#            dissub.append(i.SUBJECT.id)
#         ob_sub=subject_table.objects.filter(id__in=dissub)
#         studentlist=[]
#         for i in ob_sub:
#            ob_st=student_table.objects.filter(COURSE__id=i.COURSE.id,semester=i.semester)
#         cmd.execute(
#             "select  count(*) from timetable  inner join  courcetb  on courcetb.id=timetable.subid  inner join studtb on studtb.cource=courcetb.cource and studtb.semester=courcetb.semester where date='" + date + "' and timetable.exnid='" + exmid + "' ");
#         row = cmd.fetchone()
#         print(row)
#         if row is not None:
#             no_students = row[0];
#
#         cmd.execute("select * from hall")
#         res = cmd.fetchall()
#         if res is not None:
#             for row in res:
#                 no_seat = row[2] * 2
#                 if (no_students > no_seat):
#
#                     ad.append(row[0])
#
#
#
#
#                 else:
#
#                     ad.append(row[0])
#
#
#             cmd.execute(
#                 "select  count(*) ,studtb.cource,studtb.semester,timetable.id  from timetable  inner join  courcetb  on courcetb.id=timetable.subid  inner join studtb on studtb.cource=courcetb.cource and studtb.semester=courcetb.semester where date='" + date + "' and timetable.exnid='" + exmid + "' group by  studtb.cource");
#             res = cmd.fetchall()
#             print("res", res)
#             if res is not None:
#                 for row in res:
#                     course.append(row[1])
#                     count.append(row[0])
#                     sem.append(row[2])
#                     time.append(row[3])
#             halseat = 0;
#             divseat = 0;
#             alocstud = 0;
#             countset = 0;
#             for i in range(len(ad)):
#                 cmd.execute("select * from hall where id='" + str(ad[i]) + "'");
#                 res0 = cmd.fetchone()
#                 if res0 is not None:
#
#                     print(res0[2])
#                     halseat = int(res0[2]) * 2
#                     print(halseat)
#                     alocstud += halseat
#                     print("course", course)
#                     crsecnt = len(course)
#                     print(crsecnt)
#
#                     divseat = halseat / 5;
#                     print(divseat)
#                     seatno = 0;
#                     cou = 0;
#                     for ij in range(0, int(divseat)):
#
#                         cr = countset + ij % crsecnt;
#                         sm = countset + ij % crsecnt;
#                         tm = countset + ij % crsecnt;
#                         cmd.execute("select * from studtb where cource='" + str(course[cr]) + "' and semester='" + str(
#                             sem[
#                                 sm]) + "' and  id not in (select hall_alloc.sid from hall_alloc  where hall_alloc.schid='" + str(
#                             time[tm]) + "' )  order by studtb.id ")
#                         stud = list()
#                         res1 = cmd.fetchall()
#                         if res1 is not None:
#                             for row in res1:
#                                 stud.append(row[0])
#                         if (len(stud) == 0):
#                             cou = cou + 1
#
#                         from itertools import chain
#
#                         for j in chain(range(1, 6), range(1, len(stud) > j, 1)):
#                             seatno = (ij - cou) * 5 + j
#                             tt = countset + ij % crsecnt
#                             print(j)
#                             sttu = j - 1
#                             print("tt", tt)
#                             print("i", i)
#                             print("sttu", sttu)
#                             print("seatno", seatno)
#
#                             print("insert into hall_alloc values(null,'" + str(time[tt]) + "','" + str(
#                                 ad[i]) + "','" + str(stud[sttu]) + "','" + str(seatno) + "')")
#                             cmd.execute("insert into hall_alloc values(null,'" + str(time[tt]) + "','" + str(
#                                 ad[i]) + "','" + str(stud[sttu]) + "','" + str(seatno) + "')");
#                             con.commit()
#                     countset += divseat;
#                 if (alocstud >= no_students):
#                     break
#                 cmd.execute(
#                     "select distinct(hallid),hall.hall_number from hall_alloc inner join hall on hall.id=hall_alloc.hallid inner join timetable on timetable.id=hall_alloc.schid and timetable.exnid='" + exmid + "' and  date='" + date + "'");
#                 ss = cmd.fetchall()
#                 return render_template("seattingarrangement.html", )



from datetime import datetime, timedelta

def gentimetable(request,id):
    request.session["examid"]=id

    ob=examdetails_table.objects.filter(EXAM__id=id)

    if len(ob)==0:
        obe=examtimetable_table.objects.filter(id=id)

        sdate=obe[0].startingdate
        sem=obe[0].semester
        print(sdate,"sdate")
        cslist = []
        obcour=course_table.objects.all()
        for i in obcour:
            cslist.append(i.id)
        slist = subject_table.objects.filter(COURSE__in=cslist, semester=sem)
        sub_exmlist=[]
        sub_exm_dic=[]
        for i in slist:
            if i.subname not in sub_exmlist:
                sub_exmlist.append(i.subname)
                sub_exm_dic.append({"sub":i.subname,"count":1})
            else:
                ind=sub_exmlist.index(i.subname)
                sub_exm_dic[ind]["count"]+=1
        sorted_data = sorted(sub_exm_dic, key=lambda x: x["count"], reverse=True)
        sublist=[]
        for i in sorted_data:
            sublist.append(i['sub'])

        current_date = datetime.strptime(str(sdate), "%Y-%m-%d")


        for i in obcour:

            obs=subject_table.objects.filter(COURSE__id=i.id,semester=sem).order_by("subname")
            count=0
            print(obs,"obs")
            ssub=[]
            ssuids=[]
            for j in obs:
                ssuids.append(j.id)
                ssub.append(j.subname)
            print(sublist,"sublist")
            for k in sublist:

                time_string = "09:00:00"

                # Convert string to time
                time_object = datetime.strptime(time_string, "%H:%M:%S").time()

                ind=0
                if k in ssub:
                    ind=ssub.index(k)
                else:
                    continue
                time=""
                j=obs[ind]
                future_date = current_date + timedelta(days=count)
                print(future_date,"future_date")

                if future_date.strftime('%A')=="Friday":
                    time_string = "09:30:00"

                    # Convert string to time
                    time_object = datetime.strptime(time_string, "%H:%M:%S").time()

                if future_date.strftime('%A')=="Sunday":
                    count=count+1
                    future_date = current_date + timedelta(days=count)
                if future_date.strftime('%A') == "Saturday":
                    count = count + 2
                    future_date = current_date + timedelta(days=count)
                # future_date.strftime('%Y-%m-%d')
                # if i.exam.time=="AN":
                #     time_string = "13:00:00"
                #
                #     # Convert string to time
                #     time_object = datetime.strptime(time_string, "%H:%M:%S").time()
                #     if future_date.strftime('%A') == "Friday":
                #         time_string = "13:30:00"
                #
                #         # Convert string to time
                #         time_object = datetime.strptime(time_string, "%H:%M:%S").time()
                print("select exam")
                obexam=examdetails_table()
                obexam.EXAM = examtimetable_table.objects.get(id=id)
                obexam.SUBJECT =j
                obexam.date = future_date.strftime('%Y-%m-%d')

                obexam.time = time_object
                obexam.save()
                count+=2
                print(j,future_date.strftime('%Y-%m-%d'))
    ob = examdetails_table.objects.filter(EXAM=id)
    print(ob,"ppppppppppppppppp")
    date=['program']
    course=[]
    for i in ob:
        if str(i.date) not in date :
            date.append(str(i.date))
        if i.SUBJECT.COURSE.coursename not in course:
            course.append(i.SUBJECT.COURSE.coursename)
    res=[]
    for i in course:
        r=[[i,""]]
        for j in date:
            if j=='program':
                continue
            obt=examdetails_table.objects.filter(date=j,SUBJECT__COURSE__coursename=i,EXAM=id)
            if len(obt)>0:
                r.append([str(obt[0].SUBJECT.id),obt[0].SUBJECT.subname])
            else:
                r.append(["",""])
        res.append(r)
    print(ob,"===============")
    print(ob,"===============")
    return render(request, 'Exam Cell/view_gen_timetable.html', {'val':res,"cc":len(date),"d":date,"en":ob[0].EXAM})





























def logincode(request):
    print(request.POST)
    un = request.POST['username']
    pwd = request.POST['password']
    print(un, pwd)
    try:
        ob = login_table.objects.get(username=un, password=pwd)

        if ob is None:
            data = {"task": "invalid"}
        else:
            print("in student function")
            data = {"task": "valid", "lid": ob.id,"type":ob.type}
        r = json.dumps(data)
        print(r)
        return HttpResponse(r)
    except:
        data = {"task": "invalid"}
        r = json.dumps(data)
        print(r)
        return HttpResponse(r)




def viewallocation(request):
    lid=request.POST['lid']
    print(request.POST)
    ob=seatingarrangement_table.objects.filter(STUDENT__LOGIN_id=lid)
    print(ob,"HHHHHHHHHHHHHHH")
    mdata=[]
    for i in ob:
        data={'HALL':i.HALL.hallnumber,'seatingno':i.seatingno,'id':i.id}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status":"ok","data":mdata})

def viewtimetable(request):
    ob=examtimetable_table.objects.all()
    print(ob,"HHHHHHHHHHHHHHH")
    mdata=[]
    for i in ob:
        data={'examname':i.examname,'date':i.date,'semester':i.semester,'startingdate':i.startingdate,'status':i.status,'id':i.id}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status":"ok","data":mdata})


def viewexamdetails(request):
    did=request.POST['did']
    ob=examdetails_table.objects.filter(EXAM_id=did)
    print(ob,"HHHHHHHHHHHHHHH")
    mdata=[]
    for i in ob:
        data={'Exam':i.EXAM.examname,'Subject':i.SUBJECT.subname,'Date':i.date,'Time':i.time,'id':i.id}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status":"ok","data":mdata})



# def viewtimetable(request):
#     ob=examtimetable_table.objects.all()
#     print(ob,"HHHHHHHHHHHHHHH")
#     mdata=[]
#     for i in ob:
#         data={'examname':i.examname,'date':i.date,'semester':i.semester,'startingdate':i.startingdate,'status':i.status,'subject':i.SUBJECT.subname,'time':i.time,'id':i.id}
#         mdata.append(data)
#         print(mdata)
#     return JsonResponse({"status":"ok","data":mdata})

def viewjobdetails(request):
    ob=jobdetails_table.objects.all()
    print(ob,"HHHHHHHHHHHHHHH")
    mdata=[]
    for i in ob:
        data={'jobfile':request.build_absolute_uri(i.jobfile.url),
              'jobdescription':i.jobdescription,'posteddate':i.posteddate,'experience':i.experience,'id':i.id,"lid":i.ALUMNI.LOGIN.id}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status":"ok","data":mdata})

def viewdepartment(request):
    ob=department_table.objects.all()
    print(ob,"HHHHHHHHHHHHHHH")
    mdata=[]
    for i in ob:
        data={'deptname':i.deptname,'id':i.id}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status":"ok","data":mdata})



def alumni_registration(request):
    name=request.POST['name']
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    department = request.POST['department']
    phone = request.POST['phone']
    ob = login_table()
    ob.username = username
    ob.password = password
    ob.type = 'alumni'
    ob.save()

    obb=alumni_table()
    obb.name=name
    obb.DEPARTMENT=department_table.objects.get(id=department)
    obb.phone=phone
    obb.email=email
    obb.LOGIN=ob
    obb.save()
    return JsonResponse({"task":"valid"})




def add_job_details(request):
    lid=request.POST['lid']
    file=request.FILES['file']
    jobdescription = request.POST['jobdescription']
    experience = request.POST['experience']
    fs=FileSystemStorage()
    fp=fs.save(file.name,file)
    obb=jobdetails_table()
    obb.ALUMNI = alumni_table.objects.get(LOGIN__id=lid)
    obb.experience=experience
    obb.jobdescription=jobdescription
    obb.jobfile=fp
    obb.posteddate=datetime.now()
    obb.save()
    return JsonResponse({"status":"ok"})

# seating

def view_alumnijobdetails(request):
    lid=request.POST['lid']
    ob =jobdetails_table.objects.filter(ALUMNI__LOGIN_id=lid)
    print(ob, "HHHHHHHHHHHHHHH")
    mdata = []
    for i in ob:
        data = {'jobfile': i.jobfile.url,'jobdescription':i.jobdescription,'posteddate':i.posteddate,'experience':i.experience, 'id': i.id}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status": "ok","data":mdata})


def student_view_alumnijobdetails(request):
    ob =jobdetails_table.objects.all()
    print(ob, "HHHHHHHHHHHHHHH")
    mdata = []
    for i in ob:
        data = {'alumini':i.ALUMNI.name,'jobfile': i.jobfile.url,'jobdescription':i.jobdescription,'posteddate':i.posteddate,'experience':i.experience, 'id': i.id,"lid":i.ALUMNI.LOGIN.id}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status": "ok","data":mdata})



# def generateseat(request,d,t,timetableid):
#     request.session['d']=d
#     request.session['t']=t
#     request.session['timetableid']=timetableid
#     return redirect('/generateseat1')
# def generateseat1(request):
#
#     d=request.session['d']
#     t=request.session['t']
#     eid=request.session['eid']
#     # ob=examtimetable_table.objects.filter(date=d,time=t)
#     ob=examdetails_table.objects.filter(date=d,time=t)
#     sublist=[]
#     timetablelist=[]
#     for i in ob:
#         if i.SUBJECT.id not in sublist:
#             sublist.append(i.SUBJECT)
#
#     studlist=[]
#     studlist1=[]
#     studlist2=[]
#     # sublist shuffle
#     random.shuffle(sublist)
#     for i in sublist:
#         # ob = examtimetable_table.objects.filter(date=d, time=t,SUBJECT__id=i.id)
#         ob = examdetails_table.objects.filter(date=d,SUBJECT__id=i.id)
#         timetablelist.append(ob[0].id)
#     for i in sublist:
#         ob1=student_table.objects.filter(COURSE__id=i.COURSE.id,semester=i.semester)
#         studlist.append(len(ob1))
#         studlist1.append(len(ob1))
#         studlist2.append(ob1)
#     halllist=[]
#     halllist1=[]
#     ts=sum(studlist)
#     tscount=sum(studlist)
#     # obh=exam_hall_table.objects.filter(total_seatno__gte=ts).order_by("total_seatno")
#     # if len(obh)==0:
#     obh = list(hall_table.objects.all())
#     random.shuffle(obh)
#     for i in obh:
#         halllist.append(i)
#         halllist1.append(i.numberofseats)
#         if sum(halllist1)>=ts:
#             break
#     result=[]
#     index1=0
#     index2="na"
#     if len(studlist)>1:
#         index2=1
#     for hid in range(0,len(halllist)):
#         r={"hid":halllist[hid].room+" - "+halllist[hid].floor,"hallid":halllist[hid].id}
#         slist=[]
#         for sno in range(1,halllist[hid].numberofseats,2):
#             if tscount==0:
#                 break
#             else:
#                 if index1!="na":
#                     try:
#                         s1={"sno":sno,"tid":timetablelist[index1],"sid":studlist2[index1][studlist[index1]-studlist1[index1]].id,"sidname":studlist2[index1][studlist[index1]-studlist1[index1]].name,"sidimage":studlist2[index1][studlist[index1]-studlist1[index1]].image.url}
#                         slist.append(s1)
#                         studlist1[index1] -= 1
#                     except:
#                         s1 = {"sno": sno, "sid": 0,
#                               "sidname": "na","sidimage":'/media/nspng.png'}
#                         slist.append(s1)
#                 else:
#                     s1 = {"sno": sno, "sid": 0,
#                           "sidname": "na","sidimage":'/media/nspng.png'}
#                     slist.append(s1)
#                 if index2 != "na":
#                     try:
#                         s2={"sno":sno+1,"tid":timetablelist[index2],"sid":studlist2[index2][studlist[index2]-studlist1[index2]].id,"sidname":studlist2[index2][studlist[index2]-studlist1[index2]].name,"sidimage":studlist2[index2][studlist[index2]-studlist1[index2]].image.url}
#                         slist.append(s2)
#                         studlist1[index2]-=1
#                     except:
#                         s2 = {"sno": sno + 1, "sid": 0,
#                               "sidname": "na","sidimage":'/media/nspng.png'}
#                         slist.append(s2)
#                 else:
#                     s2 = {"sno": sno+1, "sid": 0,
#                           "sidname": "na","sidimage":'/media/nspng.png'}
#                     slist.append(s2)
#                 try:
#                     if studlist1[index1]==0:
#                         index1=index1+2
#                         if index1>len(sublist):
#                             index1="na"
#                 except:
#                     index1 = "na"
#                 try:
#                     if studlist1[index2]==0:
#                         index2=index2+2
#                         if index2>len(sublist):
#                             index2="na"
#                 except:
#                     index2="na"
#             tscount=tscount-2
#         r["slist"]=slist
#         result.append(r)
#     print(result)
#     # print(slist)
#     timetableid=request.session["timetableid"]
#     for i in result:
#         oblstaff = leave_table.objects.filter(leave_date=d)
#         lstaff = []
#         for i in oblstaff:
#             lstaff.append(i.STAFF.id)
#         hallid=i["hallid"]
#         obb=hallallocation_table.objects.exclude(id__in=lstaff)
#         res=[]
#         for j in obb:
#             res.append(j.STAFF.id)
#
#         obb1=staff_table.objects.exclude(id__in=res).exclude(id__in=lstaff)
#         if len(obb1)>0:
#             obh=hallallocation_table()
#             i['sname']=obb1[0].name
#             obh.STAFF =obb1[0]
#             obh.HALL = hall_table.objects.get(id=hallid)
#             # TIMETABLE = models.ForeignKey(examtimetable_table, on_delete=models.CASCADE)
#             obh.date=request.session['d']
#             obh.time=request.session['t']
#             obh.status='allocated'
#             obh.save()
#         else:
#             count=0
#             sid=-1
#             for kk in res:
#                 oos=hallallocation_table.objects.filter(STAFF__id=kk)
#                 if count == 0:
#                     count=len(oos)
#                     sid=kk
#                 else:
#                     if len(oos)<count:
#                         sid=kk
#                         count=len(oos)
#             obb1=staff_table.objects.filter(id=sid)
#             obh = hallallocation_table()
#             i['sname'] = obb1[0].name
#             obh.STAFF = obb1[0]
#             obh.HALL = hall_table.objects.get(id=hallid)
#             # TIMETABLE = models.ForeignKey(examtimetable_table, on_delete=models.CASCADE)
#             obh.date = request.session['d']
#             obh.time = request.session['t']
#             obh.status = 'allocated'
#             obh.save()
#
#         print(i['slist'],"lllllllllllllllllllllllllllllllllllllllll")
#
#         for j in i["slist"]:
#
#             studid=j["sid"]
#             if studid!=0:
#                 seatnumer=j["sno"]
#                 ob=seatingarrangement_table()
#                 ob.TIMETABLE_id=j['tid']
#                 ob.HALL_id=hallid
#                 ob.STUDENT_id=studid
#                 ob.seatno=seatnumer
#                 ob.save()
#
#     return render(request, 'admin/seating1.html', {"val": result})
#


def viewchat(request):
    print(request.POST)
    fromid = request.POST['from_id']
    toid=request.POST['to_id']
    ob1 = chat_table.objects.filter(FROM__id=fromid, TO__id=toid)
    ob2 = chat_table.objects.filter(FROM__id=toid, TO__id=fromid)
    combined_chat = ob1.union(ob2)
    combined_chat = combined_chat.order_by('id')
    res = []
    for i in combined_chat:
        res.append({'msg': i.msg, 'fromid': i.FROM.id, 'toid': i.TO.id, 'date':i.date})
    print(res,"===============================++++++++++++++++++++++++++++++++++========================")
    return JsonResponse({"status": "ok", "data": res})



def view_students_chat(request):
    print(request.POST)
    lid = request.POST['lid']

    ob1 = chat_table.objects.filter(FROM__id=lid)
    ids=[]
    for i in ob1:
        ids.append(i.TO.id)
    ob2 = chat_table.objects.filter(TO__id=lid)
    for i in ob2:
        ids.append(i.FROM.id)

    combined_chat = student_table.objects.filter(LOGIN__id__in=ids)
    res = []
    for i in combined_chat:
        res.append({'name': i.name, 'phno': i.phone, 'lid': i.LOGIN.id})
    print(res,"===============================++++++++++++++++++++++++++++++++++========================")
    return JsonResponse({"status": "ok", "data": res})


def sendchat(request):
    print(request.POST)
    msg=request.POST['message']
    fromid=request.POST['fromid']
    toid=request.POST['toid']
    ob=chat_table()
    ob.msg=msg
    ob.FROM=login_table.objects.get(id=fromid)
    ob.TO=login_table.objects.get(id=toid)
    ob.date=datetime.now().date()
    ob.save()
    return JsonResponse({"status": "ok"})








def seat(request):
    print("++++++++++++++++++++++++++++______________")
    print("++++++++++++++++++++++++++++______________")
    print("++++++++++++++++++++++++++++______________")
    print("++++++++++++++++++++++++++++______________")
    id=request.POST['select']
    request.session['eid']=id
    ob=examdetails_table.objects.filter(EXAM__id=id)
    res=[]
    for i in ob:
        xx=seatingarrangement_table.objects.filter(TIMETABLE__id=i.id)
        print(i.id,len(xx),"=============")
        if len(xx)>0:
            r={"date":str(i.date),"time":str(i.time),"timetableid":i.id,"st":"yes"}
            if r not in res:
                res.append(r)
        else:
            r = {"date": str(i.date), "time": str(i.time), "timetableid": i.id, "st": "no"}
            if r not in res:
                res.append(r)
    print(res)
    return render(request,'Exam Cell/seat.html',{"val":res})


def generateseat(request,d,t,timetableid):
    request.session['d']=d
    request.session['t']=t
    request.session['timetableid']=timetableid
    return redirect('/generateseat1')


def generateseat1(request):
    d=request.session['d']
    t=request.session['t']
    eid=request.session['timetableid']
    ob=examdetails_table.objects.filter(date=d,time=t)
    sublist=[]
    timetablelist=[]
    for i in ob:
        if i.SUBJECT not in sublist:
            sublist.append(i.SUBJECT)

    studlist=[]
    studlist1=[]
    studlist2=[]
    # sublist shuffle
    random.shuffle(sublist)
    sublist1=[sublist[0]]
    i=0

    while True:
        if len(sublist1)==len(sublist):
            break
        for j in sublist:
            if j not in sublist1:
                if j.COURSE.DEPARTMENT.id !=sublist1[i].COURSE.DEPARTMENT.id:
                    sublist1.append(j)
                    i=i+1
                    break
        else:
            sublist1.append(sublist[i+1])
            i=i+1
    sublist=sublist1
    for i in sublist:
        ob = examdetails_table.objects.filter(date=d, time=t,SUBJECT__id=i.id)
        timetablelist.append(ob[0].id)
    for i in sublist:
        ob1=student_table.objects.filter(COURSE__id=i.COURSE.id,semester=i.semester)
        studlist.append(len(ob1))
        studlist1.append(len(ob1))
        studlist2.append(ob1)
    halllist=[]
    halllist1=[]
    ts=sum(studlist)
    tscount=sum(studlist)
    # obh=exam_hall_table.objects.filter(total_seatno__gte=ts).order_by("total_seatno")
    # if len(obh)==0:
    obh = list(hall_table.objects.all())
    random.shuffle(obh)
    for i in obh:
        halllist.append(i)
        halllist1.append(i.numberofseats)
        if sum(halllist1)>ts:
            break
    result=[]
    index1=0
    index2="na"
    if len(studlist)>1:
        index2=1
    for hid in range(0,len(halllist)):
        r={"hid":halllist[hid].hallnumber,"hallid":halllist[hid].id}
        slist=[]
        for sno in range(1,halllist[hid].numberofseats,2):
            if tscount==0:
                break
            else:
                if index1!="na":
                    try:
                        s1={"sno":sno,"tid":timetablelist[index1],"sid":studlist2[index1][studlist[index1]-studlist1[index1]].id,"sidname":studlist2[index1][studlist[index1]-studlist1[index1]].name,"sidimage":studlist2[index1][studlist[index1]-studlist1[index1]].image.url,"crs":studlist2[index1][studlist[index1]-studlist1[index1]].COURSE.coursename}
                        slist.append(s1)
                        studlist1[index1] -= 1
                    except:
                        s1 = {"sno": sno, "sid": 0,
                              "sidname": "na","sidimage":'/media/nspng.png'}
                        slist.append(s1)
                else:
                    s1 = {"sno": sno, "sid": 0,
                          "sidname": "na","sidimage":'/media/nspng.png'}
                    slist.append(s1)
                if index2 != "na":
                    try:
                        s2={"sno":sno+1,"tid":timetablelist[index2],"sid":studlist2[index2][studlist[index2]-studlist1[index2]].id,"sidname":studlist2[index2][studlist[index2]-studlist1[index2]].name,"sidimage":studlist2[index2][studlist[index2]-studlist1[index2]].image.url,"crs":studlist2[index2][studlist[index2]-studlist1[index2]].COURSE.coursename}
                        slist.append(s2)
                        studlist1[index2]-=1
                    except:
                        s2 = {"sno": sno + 1, "sid": 0,
                              "sidname": "na","sidimage":'/media/nspng.png'}
                        slist.append(s2)
                else:
                    s2 = {"sno": sno+1, "sid": 0,
                          "sidname": "na","sidimage":'/media/nspng.png'}
                    slist.append(s2)
                try:
                    if studlist1[index1]==0:
                        index1=index1+2
                        if index1>len(sublist):
                            index1="na"
                except:
                    index1 = "na"
                try:
                    if studlist1[index2]==0:
                        index2=index2+2
                        if index2>len(sublist):
                            index2="na"
                except:
                    index2="na"
            tscount=tscount-2
        r["slist"]=slist
        result.append(r)
    print(result)
    # print(slist)
    timetableid=request.session["timetableid"]
    for i in result:

        hallid=i["hallid"]
        obb=hallallocation_table.objects.all()
        res=[]
        for j in obb:
            res.append(j.STAFF.id)

        obb1=staff_table.objects.exclude(id__in=res)
        if len(obb1)>0:
            obh=hallallocation_table()
            i['sname']=obb1[0].name
            obh.STAFF =obb1[0]
            obh.HALL = hall_table.objects.get(id=hallid)
            obh.EXAMDETAILS = examdetails_table.objects.get(id=eid)
            # TIMETABLE = models.ForeignKey(timetable_table, on_delete=models.CASCADE)
            obh.date=request.session['d']
            obh.time=request.session['t']
            obh.status='allocated'
            obh.save()
        else:
            count=0
            sid=-1
            for kk in res:
                oos=hallallocation_table.objects.filter(STAFF__id=kk)
                if count == 0:
                    count=len(oos)
                    sid=kk
                else:
                    if len(oos)<count:
                        sid=kk
                        count=len(oos)
            obb1=staff_table.objects.filter(id=sid)
            obh = hallallocation_table()
            i['sname'] = obb1[0].name
            obh.STAFF = obb1[0]
            obh.HALL = hall_table.objects.get(id=hallid)
            obh.EXAMDETAILS = examdetails_table.objects.get(id=eid)
            # TIMETABLE = models.ForeignKey(timetable_table, on_delete=models.CASCADE)
            obh.date = request.session['d']
            obh.time = request.session['t']
            obh.status = 'allocated'
            obh.save()

        print(i['slist'],"lllllllllllllllllllllllllllllllllllllllll")

        for j in i["slist"]:

            studid=j["sid"]
            if studid!=0:
                try:
                    print(j['tid'])
                    obe=examdetails_table.objects.get(id=j['tid'])
                    seatnumer=j["sno"]
                    ob=seatingarrangement_table()
                    ob.TIMETABLE_id=obe.EXAM.id
                    ob.HALL_id=hallid
                    ob.STUDENT_id=studid
                    ob.seatingno=seatnumer
                    ob.save()
                except Exception as e:
                    print("=============================================")
                    print(e)

    return render(request, 'Exam Cell\seating1.html', {"val": result})

