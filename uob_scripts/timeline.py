#
#       timeline.py
#
#       This code will create a timeline plot for a university year of all
#       assignment deadlines for all courses against key dates such as holidays
#
#
#       Things that need to be set:
#
#       year - the university year the timeline is plotted for
year = 2016
import uob_utils
import datetime
start_date = datetime.datetime.combine(uob_utils.WeekOne(year), datetime.time(0,0,0))
end_date = datetime.datetime.combine(uob_utils.DateFromUniversityWeek(year,53,0), datetime.time(0,0,0))
year_length = (end_date-start_date).days
#
#
#       bank_hol_dates - the university week number (-1) of bank holidays during
#       the academic year (I think these are fixed each year but can't find
#       confirmation of this, I am using this document as my guide:
#       https://intranet.birmingham.ac.uk/as/cladls/timetabling/documents/public/Key-to-Weeks-2017-18.pdf
bank_hol_dates = [1, 19, 32, 37, 40]
#
#
#
#
import sys
sys.path.append("../module/") # First two lines are needed for import of PyCAPI
import PyCAPI
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


capi = PyCAPI.CanvasAPI()



###############################################################################
# Retrieve data of all courses from Canvas account
#
allcourses = capi.get_courses()
accounts = [115,116,117,121] # Needed to exclude my courses from other departments
courses = []
for course in allcourses:
    if course['account_id'] in accounts:
        courses.append(course)



###############################################################################
# Retrieve data of all assignments from Canvas account
#
assignments = []
for course in courses:
    course_assignments = capi.get_assignments(course['id'])
    for assignment in course_assignments:
        if assignment['due_at'] != None:
            assignments.append({'id':assignment['id'], 'name':assignment['name'], 'course_id':assignment['course_id'], 'due_date':datetime.datetime.strptime(assignment['due_at'], '%Y-%m-%dT%H:%M:%SZ')})



###############################################################################
# Generate deadline plots for timeline
#
deadline_plot = []
for assignment in assignments:
    assignment['day_delta'] = (assignment['due_date']-start_date).days
assignments = sorted(assignments, key=lambda k: '%s' % (k['day_delta']))



###############################################################################
# Initiate plot
#
fig = plt.figure(figsize=(10,6))
ax = fig.add_subplot(111)



###############################################################################
# Plot timeline
#
ax.hlines(0,0,year_length)



###############################################################################
# Plot terms
#
term1 = [35]
term2 = [140]
term3 = [245]
term12_length = [77]
term3_length = [56]
term_ybars = [-0.2]
ax.bar(term1, term_ybars, term12_length, color='#ffd500', align='edge', label='Autumn Term', alpha=0.8)
ax.bar(term2, term_ybars, term12_length, color='#ff7500', align='edge', label='Spring Term', alpha=0.8)
ax.bar(term3, term_ybars, term3_length, color='#ff1500', align='edge', label='Summer Term', alpha=0.8)



###############################################################################
# Plot holidays
#
christ_hols = [112]
east_hols = [217]
sum_hols = [301]
chirsteast_length = [28]
sum_length = [63]
hol_ybars = [0.2]
ax.bar(christ_hols, hol_ybars, chirsteast_length, color='#00ff00', align='edge', label='Christmas Hols', alpha=0.8)
ax.bar(east_hols, hol_ybars, chirsteast_length, color='#00b100', align='edge', label='Easter Hols', alpha=0.8)
ax.bar(sum_hols, hol_ybars, sum_length, color='#008100', align='edge', label='Summer Hols', alpha=0.8)



###############################################################################
# Plot Mondays, date markers and bank holidays
#
mondays = []
date_labels = []
bank_hols = []
term = []
exam = []
for i in range(0,year_length,7):
    mondays.append(i)
    date_labels.append((start_date+datetime.timedelta(days=i)).strftime('%d %B'))
    if i/7 in bank_hol_dates:
        bank_hols.append(i)
#ax.eventplot(mondays, orientation='horizontal', colors='y', linelengths=0.4, lineoffset=0, linewidths=0.75, label='Mondays')
plt.xticks(mondays, date_labels, rotation=80, fontsize=5)
ax.scatter(bank_hols, np.zeros((len(bank_hols),), dtype=np.int), marker='x', color='k', label='Bank Holidays')


###############################################################################
# Plot deadlines
#
var = 0
for assignment in assignments:
    if year_length > (assignment['due_date']-start_date).days > 0:
        deadline_plot.append((assignment['due_date']-start_date).days)
        if len(assignment['name']) > 20:
            annotation_text = str(assignment['name'][:18]+'..')
        else:
            annotation_text = assignment['name']
        if var == 0:
            ax.annotate(annotation_text, xy=(assignment['day_delta'],0.6), xycoords='data', xytext=(assignment['day_delta'],3.9), textcoords='data', arrowprops=dict(facecolor='black', arrowstyle='-'), horizontalalignment='left', verticalalignment='top', rotation=75, fontsize=7)
            var = 1
        else:
            ax.annotate(annotation_text, xy=(assignment['day_delta'],-0.6), xycoords='data', xytext=(assignment['day_delta'],-3.9), textcoords='data', arrowprops=dict(facecolor='black', arrowstyle='-'), horizontalalignment='right', verticalalignment='bottom', rotation=75, fontsize=7)
            var = 0
ax.eventplot(deadline_plot, orientation='horizontal', colors='b', linelengths=1, lineoffset=0, linewidths=0.75, label='Assignment Deadline')



###############################################################################
# Format timeline
#
ax.set_title(label='Deadline Timetable')
plt.ylim(-5, 5)
plt.xlim(0,year_length+100)
plt.xlabel('Date (Monday)', fontsize=8)
plt.grid(axis='x', linestyle='--', alpha=0.2)
plt.gca().axes.get_yaxis().set_visible(False)
legend = plt.legend(loc='upper right')
legend.get_frame().set_alpha(1)
plt.subplots_adjust(top=0.92, bottom=0.15, left=0.05, right=0.95)
plt.savefig('timeline.png', format='png', dpi=400)
plt.show()


