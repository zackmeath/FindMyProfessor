from django.http import HttpResponse
from databasecreation import database
from django.shortcuts import *
from django.template import RequestContext
from models import Professors, Courses, OfficeHours, Comments
import datetime

def search(request):
	#get form data
    name = request.POST['lastname'].strip()
    professors = []
    profs = Professors.objects.all() #get all the professors
    #iterate throught them searching for a match
    for prof in profs:
    	if name.lower() in prof.name.lower():
    		professors.append(prof) #save the professor for later if he/she matches
    #show options:
    return render_to_response('searchresult.html', {
                'professors' : professors,
        })

def addofficehourssubmit(request, name):
	#get form data
	day = request.POST['day']
	starttime = request.POST['starttime']
	endtime = request.POST['endtime']
	prof = Professors.objects.get(name = name) #get the professor we are talking about
	insertofficehours = OfficeHours(professor = prof, day = day, starttime = starttime, endtime = endtime) #new table entry
	insertofficehours.save() #insert to DB
	return redirect('/data/' + name) #display the newly created info on the professor's page

def submitcomment(request, name):
	#get form data
	user = request.POST['user']
	comment = request.POST['comment']
	prof = Professors.objects.get(name = name) #get professor we are talking about
	comm = Comments(professor=prof,user=user,comment=comment) #create Comment entry
	comm.save() #insert into database
	return redirect('/data/' + name) #display the new data on the professor's page

def addofficehours(request,name): #office hours form
	return render_to_response('addofficehours.html',{"name":name})
def index(request): #homepage
	return render_to_response('index.html',{})
def comment(request,name): #comment form
	return render_to_response('comment.html', {"name":name})
def printDatabase(request): #show raw python dictionary (ugly, used for debugging)
	d = database()
	return HttpResponse(str(d.getDatabase()))

def insertData(request):
	#after resetting the database, this function will repopulate the tables with data
	d= database()
	teachers = d.getDatabase()
	for prof in teachers.keys():
		insertProf = Professors(name = prof)
		insertProf.save()
		for clas in teachers[prof]:
			insertclass = Courses(professor = insertProf , title = clas[0], days = clas[1], time = clas[2], location = clas[3], cid = clas[4])
			insertclass.save()
	return redirect('/') #go to the home page

def displaydatadb(request, name): #display data about the professor with name = name
	teacherclasses = []
	professor = Professors.objects.get(name=name) #get professor
	courses = Courses.objects.filter(professor=professor) #get the professor's courses
	for course in courses:
		teacherclasses.append({
			"title":course.title,
			"days":course.days,
			"time":course.time,
			"location":course.location,
			"CRN":course.cid,
			})
	oh = []
	for officehours in OfficeHours.objects.filter(professor = professor): #get office hours for the professor
		oh.append(officehours)
	comms = []
	for comment in Comments.objects.filter(professor = professor): #get comments for the professor
		comms.append(comment)
	#display all this crazy data
	return render_to_response('displaydata.html', {
                'name' : name,
                'teacherclasses' : teacherclasses,
                'officehours' : oh,
                'comments':comms,
        })

