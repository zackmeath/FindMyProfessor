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
            x+=1


        #Heres the fun part, parsing each class out - NEED MOAR SOAP!!!
        #saving data to a list of lists, called classdata

        #get a dictionary of teachers as keys and class info as values
        teachers = {}
        #last* vars are used to store the previous info, so that we can look back at it for when a lab uses that data for the class
        lasttitle = ''
        lastdays = ''
        lastlocation = ''
        lastCRN = ''
        lasttime = ''
        for classinfo in classdatalist:
            try:
                teacher = str(classinfo[16])
                location = str(classinfo[18])
                time = str(classinfo[9])
                days = str(classinfo[8])
                title = str(classinfo[7])
                CRN = str(classinfo[1])
                #above are long strings of html, parse it to get the actual data:
                location = location[location.find(">",1)+1:location.find('<',1)]
                time = time[time.find(">",1)+1:time.find('<',1)]
                days = days[days.find(">",1)+1:days.find('<',1)]
                title = title[title.find(">",1)+1:title.find('<',1)]
                CRN = CRN[30:]
                if len(CRN[CRN.find(">",1)+1:CRN.find('</a',1)]) < 10:
                    CRN = CRN[CRN.find(">",1)+1:CRN.find('</a',1)]
                elif CRN[CRN.find(">",1)+1:CRN.find('</A',1)] < 10:
                    CRN[CRN.find(">",1)+1:CRN.find('</A',1)]
                else:
                    CRN = "Unknown"
                #make days var pretty
                days = days.replace('M','monday ')
                days = days.replace('T','tuesday ')
                days = days.replace('W','wednesday ')
                days = days.replace('R','thursday ')
                days = days.replace('F','friday ')
                days = days.replace('monday','Monday')
                days = days.replace('tuesday','Tuesday')
                days = days.replace('wednesday','Wednesday')
                days = days.replace('thursday','Thursday')
                days = days.replace('friday','Friday')
                #some class titles have ampersands in them
                title = title.replace('&amp;', '&')
                #fixing weird bug in html parsing that comes up once
                if len(location)>19:
                    location = "Unknown"
                
                #in this case '&nbsp;' means that it is stealing from the last class (because is is the lab attached to it etc)
                if title.strip() == "&nbsp;":
                    title = lasttitle
                if days.strip() == "&nbsp;":
                    days = lastdays 
                if location.strip() == "&nbsp;":
                    location = lastlocation
                if CRN.strip() == "&nbsp;":
                    CRN = lastCRN 
                if time.strip() == "&nbsp;":
                    time = lasttime 
                #create the list of data 'coursedata'
                coursedata = [
                    title,
                    days,
                    time,
                    location,
                    CRN
                    ]
                #change last* vars to be known for next time
                lasttime = time
                lastlocation = location
                lastdays = days
                lasttitle = title
                lastCRN = CRN
            except:
                continue
            teacher = teacher.replace("  ", " ") #For some reason banner thinks that putting 2 spaces after the middle name is a good idea
            #now we have to parse the professors html
            #sometimes there is a weird artifact () and the if-else statement accounts for that
            if teacher.find('(',1) > teacher.find('<',1):
                teacher = teacher[teacher.find(">",1)+1:teacher.find('(',1)-1].strip()
            else:
                teacher = teacher[teacher.find(">",1)+1:teacher.find('<',1)-1].strip()
            #finally we can add the professor to the dictionary!!!
            #if-else makes sure the data is valid and simultaniously sees of the professor is already in the dictionary (to decide how to add them)
            if teacher not in teachers.keys() and len(days)!=0 and len(time)!=0 and len(location)!=0 and len(CRN)!=0 and len(title)!=0:
                teachers[teacher] = [coursedata]
            elif len(days)!= 0 and len(teacher)!=0 and len(time)!=0 and len(location)!=0  and len(CRN)!=0 and len(title)!=0:
                teachers[teacher].append(coursedata)
        return teachers #returns the dictionary where key = professor's name and value = a list of their classes (awhich are a list of data)
