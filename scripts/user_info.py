import sys
sys.path.append("../module/") # First two lines are needed for import of PyCAPI without python directory modifications
import PyCAPI
import json
import datetime
capi = PyCAPI.CanvasAPI()


"""
Function for taking the datetime string returned from Canvas
and comparaing it with computer time
"""
def overdue(assignment_due_date,current_datetime):
    is_overdue = False
    if current_datetime > assignment_due_date:
        is_overdue = True
    return is_overdue

print ''

requested_user_id = 123178
user = capi.get_user(requested_user_id)
courses = capi.get_courses()
current_datetime = datetime.datetime.now()

"""
Returns the selected users details
"""
print user['name'] + ' (ID: ' + str(user['id']) + ')'
print 'Email: ' + user['primary_email']
print ''

"""
Returns users courses
"""
print 'See user courses? y/n'
request_courses = raw_input()
print ''

if request_courses == 'y' or request_courses == 'Y' or request_courses == 'yes' or request_courses == 'Yes':
    print 'Courses enrolled on: '
    for course in courses:
        print str(course['id']) + ': ' + course['name']
    print ''

"""
Returns users assignments
"""
print 'See user assignments detail? y/n'
request_assignments = raw_input()
print ''

if request_assignments == 'y' or request_assignments == 'Y' or request_assignments == 'yes' or request_assignments == 'Yes':
    for course in courses:
        print str(course['id']) + ': ' + course['name']
        assignments = capi.get_assignments(course['id'])
        print '     Published:'
        for assignment in assignments:
            print '         ' + str(assignment['id']) + ': ' + assignment['name']
            print '             Type: ' + json.dumps(assignment['submission_types'])
            print '             Grading type: ' + assignment['grading_type']
            print '             Marks available: ' + str(assignment['points_possible'])
            print '             Unlocked at: ' + str(assignment['unlock_at'])
            print '             Due at: ' + str(assignment['due_at'])
            print '             Submitted: ' + str(assignment['has_submitted_submissions'])
        print ''
    print ''

"""
Get course details - teacher
"""
print 'See courses enrolled as teacher? y/n'
request_teacher_courses = raw_input()
print ''

if request_teacher_courses == 'y' or request_teacher_courses == 'Y' or request_teacher_courses == 'yes' or request_teacher_courses == 'Yes':
    print 'Courses enrolled on as teacher:'
    for count in range(0,len(courses)):
        if courses[count]['enrollments'][0]['type'] == 'teacher':
            print str(courses[count]['id']) + ': ' + courses[count]['name']
    print ''


"""
Returns users overdue assignments
"""
print 'Check for overdue assignments? y/n'
request_overdue = raw_input()
print ''

if request_overdue == 'y' or request_overdue == 'Y' or request_overdue == 'yes' or request_overdue == 'Yes':
    overdue_assignment_no = 0
    for course in courses:
        print str(course['id']) + ': ' + course['name']
        assignments = capi.get_assignments(course['id'])
        print '     Overdue:'
        for assignment in assignments:
            if str(assignment['due_at']) != 'None':
                assignment_due_date = datetime.datetime.strptime(assignment['due_at'], '%Y-%m-%dT%H:%M:%SZ')
                is_overdue = overdue(assignment_due_date,current_datetime)
                if is_overdue and str(assignment['has_submitted_submissions']) == 'False':
                    print '         ' + str(assignment['id']) + ': ' + assignment['name']
                    print '             Type: ' + json.dumps(assignment['submission_types']) 
                    print '             Due at: ' + str(assignment_due_date)
                    overdue_assignment_no = overdue_assignment_no + 1
        print ''
    print 'Number of overdue assignments: ' + str(overdue_assignment_no)
    print ''

"""
Returns submission details for user submissions
This section is commented out because the get_user_submission_details
function does not work in PyCAPI as no information is returned
"""
"""
print 'See user submission summary? y/n'
request_user_submission_summary = raw_input()
print ''

if request_user_submission_summary == 'y' or request_user_submission_summary == 'Y' or request_user_submission_summary == 'yes' or request_user_submission_summary == 'Yes':
    for course in courses:
        print str(course['id']) + ': ' + course['name']
        assignments = capi.get_assignments(course['id'])
        for assignment in assignments:
            print '     ' + str(assignment['id']) + ': ' + assignment['name']
            user_submission_details = capi.get_user_submission_details(course['id'],assignment['id'],requested_user_id)
            print user_submission_details
            for submission_details in user_submission_details:
                print '         Score: ' + str(submission_details['score'])
                print '         Out of: ' + str(assignment['points_possible'])
                print '         Late: ' + str(submission_details['late'])
"""

"""
Returns users notifications summary
"""
print 'See user notification activity summary? y/n'
request_activity_summary = raw_input()
print ''

if request_activity_summary == 'y' or request_activity_summary == 'Y' or request_activity_summary == 'yes' or request_activity_summary == 'Yes':
    user_activity_summary = capi.get_user_activity_summary()
    print 'User notification activity summary: | Total(Unread)'
    for activity_summary in user_activity_summary:
        if activity_summary['type'] == 'DiscussionTopic':
            print 'Discussion topic: ' + str(activity_summary['count']) + '(' + str(activity_summary['unread_count']) + ')'
        elif str(activity_summary['notification_category']) != 'None':
            print activity_summary['type'] + ' (' + activity_summary['notification_category'] + '): ' + str(activity_summary['count']) + '(' + str(activity_summary['unread_count']) + ')'
        else:
            print activity_summary['type'] + ': ' + str(activity_summary['count']) + '(' + str(activity_summary['unread_count']) + ')'
    print ''

       


