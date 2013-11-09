from django.db import models

class Professors(models.Model):
    name = models.CharField(max_length=50)

class Courses(models.Model):
    cid = models.CharField(primary_key = True, max_length = 15)
    professor = models.ForeignKey(Professors)
    title = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    days = models.CharField(max_length=70)
    location = models.CharField(max_length=20)

class OfficeHours(models.Model):
	professor = models.ForeignKey(Professors)
	starttime = models.CharField(max_length=50)
	endtime = models.CharField(max_length=50)
	day = models.CharField(max_length=50)

class Comments(models.Model):
	professor = models.ForeignKey(Professors)
	user = models.CharField(max_length=50)
	comment = models.CharField(max_length=1000)
	time = models.DateTimeField(auto_now = True)