from BeautifulSoup import BeautifulSoup
class database:
    def __inti__(self):
        pass
    def getDatabase(self):
        #open courseHTML.html which is the html taken from banner,
        #has the data for all the classes, aka the professor's schedule
        document = open('coursesHTML.html','r')
        document = document.readlines()

        #soup object allows python to parse HTML easily
        soup = BeautifulSoup(''.join(document))
        #print soup.prettify() #prints EVARYTHANG but pretty-ified

        #each class has a row in a giant table
        tablerows = soup.findAll('tr')

        #tablerows - classes are from tablerows[9] to tablerows[2504]
        #save them to a big list called classdatalist
        x = 9
        classdatalist = []
        while x<=2504:
            soup2 = BeautifulSoup(''.join(str(tablerows[x])))
            classdatalist.append(soup2.findAll('td'))
            # print x
            x+=1
        # for thing in classdatalist[0]:
            # print thing
        #Heres the fun part, parsing each class out - NEED MOAR SOAP!!!
        #saving data to a list of lists, called classdata

        #get a dictionary of teachers as keys and class info as values
        teachers = {}
        for classinfo in classdatalist:
            try:
                teacher = str(classinfo[16])
                location = str(classinfo[18])
                time = str(classinfo[9])
                days = str(classinfo[8])
                location = location[location.find(">",1)+1:location.find('<',1)]
                time = time[time.find(">",1)+1:time.find('<',1)]
                days = days[days.find(">",1)+1:days.find('<',1)]
                coursedata = [
                    days,
                    time,
                    location,
                    ]
            except:
                continue
            if teacher.find('(',1) > teacher.find('<',1):
                teacher = teacher[teacher.find(">",1)+1:teacher.find('(',1)-2]
            else:
                teacher = teacher[teacher.find(">",1)+1:teacher.find('<',1)-2]
            teacher=teacher.replace(" ", "")
            if teacher not in teachers.keys() and len(days)!=0 and len(time)!=0 and len(location)!=0:
                teachers[teacher] = [coursedata]
            elif len(days)!= 0 and len(teacher)!=0 and len(time)!=0 and len(location)!=0 :
                teachers[teacher].append(coursedata)
        # for teacher in teachers:
        #     print teacher + ':'
        #     for classinfo in teachers[teacher]:
        #         print classinfo
        return teachers
