from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
import getpass,os,click
from operator import itemgetter
import HTMLParser
h= HTMLParser.HTMLParser()

login_url = 'http://codechef.com'



def inPre(s):
	try:
		s = s.split('<pre>')[1].split('</pre>')[0]
	except:
		s = s.split('<b>')[1].split('</b>')[0]
	return s
def getQuesFromList(directory):
	browser.open(login_url+directory)
	#probs = browser.find_all(class_='problemname')
	z=1
	#print type(browser.find_all(class_='problemname', href=True))
	subAccRMS = 0
	probs = browser.find_all(class_='problemrow')
	sm = 0
	formattedProbs = []
	
	for i in probs:
		s=getInner(str(i))
		s.append(float(s[2])*float(s[3]))
		formattedProbs.append(s)

	formattedProbs = sorted(formattedProbs, key=itemgetter(4),)

	click.secho("%-5s" % ("#") ,nl=False, bold=True)
	click.secho("%-20s" % ("Code") ,nl=False, bold=True)
	click.secho("%-55s" % ("Name"), nl=False, bold=True)
	click.secho("%-30s" % ("Successful Submissions"), nl=False, bold=True)
	click.secho("%-20s" % ("Accuracy"), nl=False ,bold=True)
	click.secho("%-20s" % ("Accuracy X Successful Submissions"), fg="white" ,bold=True)
	click.echo()
	n = len(formattedProbs)
	for i in formattedProbs:
		name,short,submissions,accuracy,subAcc = i
		color = 'red'
#		if float(accuracy) * float(submissions) > subAccMedian:
#			color = 'yellow'
#		if float(accuracy) * float(submissions) > subAccMedian/2:
#			color = 'green'
		click.secho("%-5s" % (n) ,nl=False, bold=True)
		click.secho("%-20s" % (short) ,nl=False, bold=True)
		click.secho("%-55s" % (name), nl=False, bold=True)
		click.secho("%-30s" % (submissions), nl=False, bold=True)
		click.secho("%-20s" % (accuracy), nl=False ,bold=True)
		click.secho("%-20s" % (subAcc), fg=color ,bold=True)
		n-=1
	return formattedProbs


def getQues(ques,tries):
	if(tries==2):
		return ""
	browser.open("https://www.codechef.com/problems/" + ques)
	z = browser.find_all(class_="content")
	if(len(z)>=3):
		return str(browser.parsed)," ".join(getInner(str(z[3]))).replace("&lt;","<").replace("&gt;",">")
	else:
		return getQues(ques,tries+1)

def openShell():
	os.system("bash")
def getTemplate():
	f = open('Template/default.cpp','r')
	return f.read()

def getInner(s):
	a=[]
	x=""
	i=0
	flag=0
	while i<len(s):
		if s[i] == '<':
			if x!="" and  x!="\n":
				a.append(x)
				x=""
			flag+=1
		elif s[i] == '>':
			flag-=1
		elif flag==0 and s[i]!="\n":
			x+=s[i]
		i+=1
	if x!="" and x!="\n":
		a.append(x)
	return a

practiceLink = {}

practiceLink[1] = "/problems/school"
practiceLink[2] = "/problems/easy"
practiceLink[3] = "/problems/medium"
practiceLink[4] = "/problems/hard"

def getPractice():
	while(1):
		print "1. Beginner"
		print "2. Easy"
		print "3. Medium"
		print "4. Hard"
		print "5. Shell"
		print "99. Back"
		option = input()
		if option != 99:
			qarr = getQuesFromList(practiceLink[int(option)])
			while 1:
				print "To select question, enter ques code to view '99' to go back or '#' to go to shell, 'vi filename' to load in vim"
				option = raw_input()
				if(option=='99'):
					break
				elif(option=='#'):
					os.system('bash')
				elif(option.split()[0]=='vi'):
					raw,quesStr = getQues(option.split('.')[0].split()[1],0)
					os.system("echo \"/*" + quesStr + "*/ \\n" + getTemplate() +"\" > Codes/" + option.split()[1])
					try:
						os.system("echo \"" + inPre(raw.split('Input')[1].split('Output')[0]) + "\" >  Codes/" + option.split()[1].split('.')[0] + ".in")
						os.system("echo \"" + inPre(raw.split('Output')[1].split('Author:')[0]) + "\" >  Codes/" + option.split()[1].split('.')[0] + ".out")
					except:
						pass
					os.system('vi Codes/' + option.split()[1])
				elif(option.split()[0]=="run"):
					os.system("echo Sample Input : ")
					os.system("cat "+option.split()[1]+".in")
					os.system("echo Sample Output : ")
					os.system("cat "+option.split()[1]+".out")
					os.system("g++ -o "+option.split()[1]+" option.split()[1]"+".cpp")
					os.system("./"+option.split()[1])
				try:
					qu = getQues(option,0)
					click.secho(qu,bold=True)
				except:
					pass
		elif(option==2):
			pass
		elif(option==3):
			pass
		elif(option==4):
			pass
		elif(option==5):
			openShell()
		else:
			return

browser = RoboBrowser(parser="lxml")
browser.open(login_url)



form = browser.get_form(id='new-login-form')


#form['name'].value = raw_input("Please enter username : ") #"moulik_nitd"
#form['pass'].value = getpass.getpass("Please enter password : ") #"wWZQebK5Ap"
#browser.submit_form(form)
#Logged in

user = browser.find(class_='right')

print " ".join(user.text.split('Account')[0].replace('\n','').split())

while 1:
	print "1. Practice"
	print "2. Contests"
	print "3. Shell"
	print "4. Show question from question code"
	print "99. Logout"
	option = input()
	if(option==1):
		getPractice()
	elif(option==2):
		getContests()
	elif(option==3):
		openShell()
	elif(option==4):
		getQues(raw_input("Input question code"))
	else:
		exit()


