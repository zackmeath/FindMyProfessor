from django.http import HttpResponse
from databasecreation import database
from django.shortcuts import *
from django.template import RequestContext
from models import Professors, Courses, OfficeHours
import datetime

def search(request):
    name = request.POST['lastname']
    professors = []
    profs = Professors.objects.all()
    for prof in profs:
    	if name.lower() in prof.name.lower():
    		professors.append(prof)
    return render_to_response('searchresult.html', {
                'professors' : professors,
        })
def addofficehourssubmit(request, name):
	day = request.POST['day']
	starttime = request.POST['starttime']
	endtime = request.POST['endtime']
	prof = Professors.objects.get(name = name)
	insertofficehours = OfficeHours(professor = prof, day = day, starttime = starttime, endtime = endtime)
	insertofficehours.save()
	
	return redirect('/data/' + name)

def addofficehours(request,name):
	return render_to_response('addofficehours.html',{"name":name})
def index(request):
	return render_to_response('index.html',{})
def printDatabase(request):
	d = database()
	teachString = str(d.getDatabase())
	return HttpResponse(teachString)

def insertData(request):
	d= database()
	teachers = d.getDatabase()
	for prof in teachers.keys():
		insertProf = Professors(name = prof)
		insertProf.save()
		for clas in teachers[prof]:
			insertclass = Courses(professor = insertProf , title = clas[0], days = clas[1], time = clas[2], location = clas[3], cid = clas[4])
			insertclass.save()
	return redirect('/')

def displaydatadb(request, name):
	teacherclasses = []
	professor = Professors.objects.get(name=name)
	courses = Courses.objects.filter(professor=professor)
	for course in courses:
		teacherclasses.append({
			"title":course.title,
			"days":course.days,
			"time":course.time,
			"location":course.location,
			"CRN":course.cid,
			})

		# teacherclasses.append({
		# 	"title":classes[0],
		# 	"days":classes[1],
		# 	"time":classes[2],
		# 	"location":classes[3],
		# 	"CRN":classes[4]
		# 	})
	oh = []
	for officehours in OfficeHours.objects.filter(professor = professor):
		oh.append(officehours)
	return render_to_response('displaydata.html', {
                'name' : name,
                'teacherclasses' : teacherclasses,
                'officehours' : oh,
        })

