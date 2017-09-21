#
#       assignment_update.py
#
#       This code will update assignments rolled over from the previous year
#       to have matching academic calandar deadlines for the new year
#
#
#       Things that need to be set:
#
#       new_term - name of new academic term that deadlines need to be
#       updated for ie.'2017/18' with the format yyyy/yy
new_term = '2017/18'
new_year = int(new_term[:4])
#
#
#
#
import sys
sys.path.append("../module/") # First two lines are needed for import of PyCAPI
import PyCAPI
import uob_utils
import datetime
import json



capi = PyCAPI.CanvasAPI()
today = datetime.datetime.now()
current_year = today.year



###############################################################################
# Retrieve data of all courses from Canvas account
#
include = ['term']
courses = capi.get_courses(include=include)



###############################################################################
# Retrieve data of all assignments from Canvas account
#
assignments = []
for course in courses:
    course_assignments = capi.get_assignments(course['id'])
    for assignment in course_assignments:
        if assignment['due_at'] != None and assignment['unlock_at'] != None and assignment['lock_at'] != None:
            assignments.append({'id':assignment['id'], 'course_id':assignment['course_id'], 'term':course['term']['name'], 'due_datetime':datetime.datetime.strptime(assignment['due_at'], '%Y-%m-%dT%H:%M:%SZ'), 'unlock_datetime':datetime.datetime.strptime(assignment['unlock_at'], '%Y-%m-%dT%H:%M:%SZ'), 'lock_datetime':datetime.datetime.strptime(assignment['lock_at'], '%Y-%m-%dT%H:%M:%SZ')})
        if assignment['due_at'] != None and (assignment['unlock_at'] == None or assignment['lock_at'] == None):
            if assignment['unlock_at'] != None and assignment['lock_at'] == None:
                assignments.append({'id':assignment['id'], 'course_id':assignment['course_id'], 'term':course['term']['name'], 'due_datetime':datetime.datetime.strptime(assignment['due_at'], '%Y-%m-%dT%H:%M:%SZ'), 'unlock_datetime':datetime.datetime.strptime(assignment['unlock_at'], '%Y-%m-%dT%H:%M:%SZ'), 'lock_datetime':None})
            if assignment['unlock_at'] == None and assignment['lock_at'] != None:
                assignments.append({'id':assignment['id'], 'course_id':assignment['course_id'], 'term':course['term']['name'], 'due_datetime':datetime.datetime.strptime(assignment['due_at'], '%Y-%m-%dT%H:%M:%SZ'), 'unlock_datetime':None, 'lock_datetime':datetime.datetime.strptime(assignment['lock_at'], '%Y-%m-%dT%H:%M:%SZ')})
            else:
                assignments.append({'id':assignment['id'], 'course_id':assignment['course_id'], 'term':course['term']['name'], 'due_datetime':datetime.datetime.strptime(assignment['due_at'], '%Y-%m-%dT%H:%M:%SZ'), 'unlock_datetime':None, 'lock_datetime':None})



###############################################################################
# Update deadlines for out of date assignments
#
for assignment in assignments:
    if assignment['term'] == new_term:
        if uob_utils.AcademicYear(assignment['due_datetime'].date()) == new_year-1:
            new_deadline = PyCAPI.datetime2unicode(datetime.datetime.combine(uob_utils.FindCorrespondingDate(assignment['due_datetime'].date(),new_year),assignment['due_datetime'].time()))
            parameter = 'due_at'
            capi.update_assignment(assignment['course_id'], assignment['id'], parameter, value=new_deadline)
            if assignment['unlock_datetime'] != None:
                new_unlock = PyCAPI.datetime2unicode(datetime.datetime.combine(uob_utils.FindCorrespondingDate(assignment['unlock_datetime'].date(),new_year),assignment['unlock_datetime'].time()))
                parameter = 'unlock_at'
                capi.update_assignment(assignment['course_id'], assignment['id'], parameter, new_unlock)
            if assignment['lock_datetime'] != None:
                new_lock = PyCAPI.datetime2unicode(datetime.datetime.combine(uob_utils.FindCorrespondingDate(assignment['lock_datetime'].date(),new_year),assignment['lock_datetime'].time()))
                parameter = 'lock_at'
                capi.update_assignment(assignment['course_id'], assignment['id'], parameter, new_lock)




