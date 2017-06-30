import calendar
import datetime
import math
import smtplib
import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate


class MailAPI():
	""""""
	def __init__(self, username=None, password=None, server='smtp.gmail.com', port=465, path_to_credentials='~/.mailcredentials'):
		if username == None or password==None: # if username and password are not specified, look for .mailcredentials file
			if not os.path.isfile(os.path.expanduser(path_to_credentials)):
				raise RuntimeError('Provide a username and password in ~/.mailcredentials or as an argument of the call.')
			if int(oct(os.stat(os.path.expanduser(path_to_credentials)).st_mode)[-3:]) > 600: # check that .canvastoken file has appropriate file restrictions
				raise RuntimeError('Permissions of mail credentials are not secure enough.')
			with open(os.path.expanduser(path_to_credentials)) as f: # read Canvas token from .canvastoken file
				lines = f.readlines()
			username = lines[0].strip()
			password = lines[1].strip()
		try:
			self.ssl = smtplib.SMTP_SSL(server, port)
			self.ssl.ehlo()
			self.ssl.login(username, password)	
		except:
			raise RuntimeError('Could not connect to e-mail server.')
		
	def send(self, from_addr, to_addr, msg):
		return self.ssl.sendmail(from_addr, to_addr, msg.as_string())


class EMailMessage(MIMEMultipart):
	""""""
	def __init__(self, from_addr, to_addr, subj):
		MIMEMultipart.__init__(self)
		self['From'] = from_addr
		self['To'] = to_addr
		self['Date'] = formatdate(localtime=True)
		self['Subject'] = subj
	
	def body(self, text):
		self.attach(MIMEText(text))

	def attach_file(self, path_to_file):
		with open(path_to_file, 'rb') as f:
			part = MIMEApplication(f.read(),Name=os.path.basename(path_to_file))
			part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(path_to_file)
		self.attach(part)


def AugustBankHoliday(year):
	"""Returns the date of the August Bank Holiday for a given year."""
	cal = calendar.Calendar()
	month = cal.monthdatescalendar(year,8)
	lastweek = month[-1]
	monday = lastweek[0]
	return monday

def WeekOne(year):
	"""Returns the Monday of week 1 for a given academic year (e.g. 2014 for 14/15)."""
	cal = calendar.Calendar(4)
	month = cal.monthdatescalendar(year,8)
	lastweek = month[-1]
	friday = lastweek[0]
	monday = friday - datetime.timedelta(days=4)
	return monday

def UniversityWeek(date):
	"""Returns the university week for a given date"""
	if date >= WeekOne(date.year):
		return int(math.floor((date-WeekOne(date.year)).days/7))+1
	else:
		return int(math.floor((date-WeekOne(date.year-1)).days/7))+1

def DateFromUniversityWeek(ayear,uweek,dow):
	"""Takes the academic year (e.g. 2014 for 14/15), university week and day of the week (e.g. Mon = 0, Tues = 1, etc.) as input and returns a date."""
	return WeekOne(ayear) + datetime.timedelta(weeks=uweek-1) + datetime.timedelta(days=dow)

def AcademicYear(date):
	"""Returns the academic year for a given date."""
	if date >= WeekOne(date.year):
		return date.year
	else:
		return date.year - 1

def TermWeek(date):
	"""Returns a list that contains the term, term week and university week for a given date."""
	uweek = UniversityWeek(date)
	if uweek <= 16 and uweek >= 5:
		return [1,uweek-5,uweek]
	elif uweek <= 31 and uweek >= 21:
		return [2,uweek-20,uweek]
	elif uweek <= 43 and uweek >= 36:
		return [3,uweek-35,uweek]
	else:
		return [0,0,uweek]

def FindCorrespondingDate(date,ayear):
	"""Returns a date in any academic year that corresponds to the input date for its academic year."""
	return DateFromUniversityWeek(ayear,UniversityWeek(date),date.weekday())
	
