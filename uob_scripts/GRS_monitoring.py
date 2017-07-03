from openpyxl import load_workbook
import sys
sys.path.append("../module/") # First two lines are needed for import of PyCAPI
import PyCAPI
import datetime
import math
import json
import os
import smtplib
from email.mime.text import MIMEText
import calendar


#course_id = '7054'
course_id = '24191'

wb = load_workbook('GRS_monitoring_sheet.xlsx')
ws = wb['Sheet1']

"""
currenttime = datetime.date.today()
currentday = currenttime.day # returns day date integer
currentweekday = datetime.date.weekday(currenttime) # returns weekday as integer, 0 being Monday, 1 being Tuesday etc.
monthfirst = currenttime.replace(day = 1) # gets datetime of first day of current month
monthfirstweekday = datetime.date.weekday(monthfirst) # gets weekday as integer of first day of month

if currentweekday-monthfirstweekday >= -1: # ie. start of month = Thu and current = Wed/start of month = Wed and current = Fri
    workingdays = (math.floor(currentday/7)*5) + (currentday%7)
elif monthfirstweekday == 6: # accounts for extra day of Sunday given in original calculation
    workingdays = ((math.floor(currentday/7)*5) + (currentday%7)) - 1
else: # ie. start of month = Thu and current = Mon/start of month = Sat and current = Tue
    workingdays = ((math.floor(currentday/7)*5) + (currentday%7)) - 2
print 'Working days since start of month: ' + str(workingdays)
"""

# I think this now works - so I pasted it in instead of the above
todaydate = datetime.date.today()
firstdate = todaydate.replace(day=1)
workingday = ((todaydate.day - max(5 - firstdate.weekday(),0) - min(todaydate.weekday()+1,5))/7)*5 + max(5 - firstdate.weekday(),0) + min(todaydate.weekday()+1,5)
print 'Current business day of the month: ' + str(workingday)

# I do not understand why you need to have two separate lists. I would opt for a list of dictionaries:
students = []
i = 2
while ws['A'+str(i)].value != None:
    students.append({'name':ws['A'+str(i)].value, 'id':ws['B'+str(i)].value, 'supervisor_name':ws['C'+str(i)].value, 'supervisor_id':ws['D'+str(i)].value, 'skip': False})
    if ws['E'+str(i)].value != None: # I would not ask for zeros and ones - just check if cell contains something
        students[-1]['skip'] == True
    i += 1   
#print json.dumps(students, indent=2)

capi = PyCAPI.CanvasAPI()
for student in students:
    student['canvas_id'] = capi.get_user('sis_login_id:'+str(student['id']))['id']
    student['email'] = capi.get_user('sis_login_id:'+str(student['id']))['primary_email']
    student['supervisor_email'] = capi.get_user('sis_login_id:'+str(student['supervisor_id']))['primary_email']
#print json.dumps(students, indent=2)

# I think at this point you want to see whether each student has a submission to the current assignment and whether it was marked complete...

# First we need to find the current assignment:
"""
payload = {}
payload['bucket'] = 'upcoming'
assignments = capi.get('/courses/%s/assignments' % course_id, payload = payload)

if len(assignments) == 1:
    assignment_id = assignments[0]['id']
else:
    raise RuntimeError('I could not find the current assignment.')
#print json.dumps(assignment, indent=2)


# Second, we can loop though all users in Excel sheet
for student in students:
    # Step 1...download details of submission for the user
    submission = capi.get_assignment_submissions(course_id, assignment_ids=assignment_id, user_ids=student['canvas_id'], grouped=False)
    # Step 2...check whether form has been uploaded
    if 'attachments' in submission[0]['submissions'][0]:
        student['form'] = True
    else:
        student['form'] = False
    # Step 3...check whether submission has been marked as complete
    if 'grade' in submission[0]['submissions'][0]:
        if submission[0]['submissions'][0]['grade'] == 'complete':
            student['complete'] = True
        else:
            student['complete'] = False
    else:
        student['complete'] = False
    
print json.dumps(students, indent=2)
"""


# Using deadlines to get current assignment
assignments = capi.get_assignments(course_id)
for assignment in assignments:
    if todaydate.month == datetime.datetime.strptime(assignment['due_at'], '%Y-%m-%dT%H:%M:%SZ').month:
        assignment_id = assignment['id']
    next_assignment = False
    if todaydate.month+1 == datetime.datetime.strptime(assignment['due_at'], '%Y-%m-%dT%H:%M:%SZ').month:
        next_assignment = True

for student in students:
    # Step 1...download details of submission for the user
    submission = capi.get_assignment_submissions(course_id, assignment_ids=assignment_id, user_ids=student['canvas_id'], grouped=False)
    # Step 2...check whether form has been uploaded
    if 'attachments' in submission[0]['submissions'][0]:
        student['form'] = True
    else:
        student['form'] = False
    # Step 3...check whether submission has been marked as complete
    if 'grade' in submission[0]['submissions'][0]:
        if submission[0]['submissions'][0]['grade'] == 'complete':
            student['complete'] = True
        else:
            student['complete'] = False
    else:
        student['complete'] = False

"""
# Sending emails based on assignment completion
# Obtain SMTP username and password, and other email details. Connect to server.
if not os.path.isfile(os.path.expanduser('~/.mailcredentials')):
    raise RuntimeError('Make sure ~/.mailcredentials exists in home directory.')
if int(oct(os.stat(os.path.expanduser('~/.mailcredentials')).st_mode)[-3:]) > 600:
    raise RuntimeError('Permissions of ~/.mailcredentials are not secure enough.')
with open(os.path.expanduser('~/.mailcredentials')) as f:
    lines = f.readlines()
username = lines[0].strip()
password = lines[1].strip()
try:
    server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server_ssl.ehlo()
    server_ssl.login(username, password)
    #server_ssl.set_debuglevel(1) # When set to true (1) will print debug messages for connection
except:
    raise RuntimeError('Could not connect to GMAIL server.')
"""

# Sending emails based on GRS assignment completion
recipients = []
#PG_email = # Enter Head of PG studies email here
#school_email = # Enter Head of School email here
for student in students:
    # If file has not been uploaded and complete mark is missing
    if student['form'] == False and student['complete'] == False:
        if workingday in (1,10,15):
            print 'Email student'
            recipients.append(student['email'])
        elif 11<=workingday<=14:
            print 'Email student and supervisor'
            recipients.extend((student['email'], student['supervisor_email']))
        elif 15<=workingday<=17:
            print 'Email student, supervisor and Head of PG studies'
            recipients.extend((student['email'], student['supervisor_email'], PG_email))
        elif 18<=workingday<=19:
            print 'Email student, supervisor, Head of PG studies and Head of School'
            recipients.extend((student['email'], student['supervisor_email'], PG_email, school_email))
        else:
            print 'No reminder emails need to be sent'
    # If file has been uploaded but complete mark is missing
    elif student['form'] == True and student['complete'] == False:
        if 11<=workingday<=14:
            print 'Email supervisor'
            recipients.append(student['supervisor_email'])
        elif 15<=workingday<=17:
            print 'Email supervisor and Head of PG studies'
            recipients.extend((student['supervisor_email'], PG_email))
        elif 18<=workingday<=19:
            print 'Email supervisor, Head of PG studies and Head of School'
            recipients.extend((student['supervisor_email'], PG_email, school_email))
        else:
            print 'No reminder emails need to be sent'
    # If it is marked as complete, but file is not uploaded, unmark as complete
    elif student['form'] == False and student['complete'] == True:
        print 'Mark as incomplete'
    else:
        print 'No reminder emails need to be sent'

# If it is the 10th of the month or past the 10th of the month, send summary email
if workingday == 10:
    print 'Send summary email'
    recipients.append(PG_email)
    msg = MIMEText('Enter email text here')

"""
comma_space = ', '
msg = MIMEText('Insert email text here')
msg['Subject'] = 'GRS Reminder'
msg['From'] = username
msg['To'] = comma_space.join(recipients)

try:
    server_ssl.sendmail(username, recipients, msg.as_string())
    print 'Email sent successfully'
    server_ssl.quit()
except:
    print 'Email unable to send'
"""

workingday = 20
next_assignment = False
# Check whether an assignment is present for the following month
if workingday == 20 and next_assignment == False: # New assignment needed for next month
    current_assignment = capi.get_assignment(course_id, assignment_id)
    print current_assignment
    payload = {}
    #payload['assignment[name]'] = calendar.month_name[datetime.datetime.strptime(current_assignment['due_at'], '%Y-%m-%dT%H:%M:%SZ').month+1]
    #payload['submission_types'] = 'online_upload'
    #payload['points_possible'] = 0.0
    #payload['grading_type'] = 'pass_fail'
    #payload['unlock_at'] =
    #payload['lock_at'] = 
    #payload['due_at'] =
    for key in current_assignment:
        payload['assignment['+key+']'] = current_assignment[key]
    print json.dumps(payload, indent=2)
    #capi.post('/courses/%s/assignments' % course_id, payload=payload)



