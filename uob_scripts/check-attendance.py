#
#		check-attendance.py
#
#		This code checks interaction by students with a particular
#		course over a period of time.
#
#
course_id = 34797
course_id = 35270
year = 2018
#
#
import sys
sys.path.append("../module/")
import PyCAPI
import datetime
import json
import uob_utils
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages


pp = PdfPages('multipage.pdf')

start_date = datetime.datetime.combine(uob_utils.DateFromUniversityWeek(year,6,0), datetime.time(0,0,0))
end_date = datetime.datetime.combine(uob_utils.DateFromUniversityWeek(year,17,0), datetime.time(0,0,0))

capi = PyCAPI.CanvasAPI()

all_students = capi.get_users(course_id, enrollment_type=['student'])

for student in all_students:
	print ' '
	print ' '
	print ' '
	print student
	activity = capi.get_student_activity_on_course(course_id, student['id'])
	course_page_views = []
	for key in activity['page_views'].keys():
		timestamp = datetime.datetime.strptime(key[0:19], "%Y-%m-%dT%H:%M:%S")
		count = activity['page_views'][key]
		course_page_views.append([timestamp,count])
	course_page_views.sort(key=lambda x: x[0])
	student['course_page_views'] = course_page_views
	timestamps = []
	views = []
	wtimestamps = []
	wviews = []
	ttimestamps = []
	tviews = []
	for page_view in student['course_page_views']:
		print page_view
		if page_view[0].weekday() == 2 and page_view[0].hour == 9:
			wtimestamps.append(page_view[0])
			wviews.append(page_view[1])
		elif page_view[0].weekday() == 3 and page_view[0].hour == 9:
			ttimestamps.append(page_view[0])
			tviews.append(page_view[1])
		else:
			timestamps.append(page_view[0])
			views.append(page_view[1])
	fig = plt.figure(figsize=(8,3))
	ax = fig.add_subplot(111)
	ax.bar(timestamps, views, color='black')
	ax.bar(wtimestamps, wviews)
	ax.bar(ttimestamps, tviews)
	ax.xaxis_date()
	ax.set_ylim(0,120)
	ax.set_xlim(start_date,end_date)
	ax.xaxis.set_major_locator(matplotlib.dates.WeekdayLocator(byweekday=matplotlib.dates.MO))
	ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%d-%m-%y'))
	ax.set_xlabel('Date')
	ax.set_ylabel('Views')
	ax.set_title(student['name'] + ' (' + student['sis_user_id'] + ')')
	fig.autofmt_xdate()
	plt.savefig(pp, format='pdf')
pp.close()

	

