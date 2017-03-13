import PyCAPI
import json
import datetime
capi = PyCAPI.CanvasAPI()

################################################################################

def overdue(assignment_due_date_string,current_datetime):
    is_overdue = False
    
    if int(assignment_due_date_string[0:4]) < int(current_datetime[0:4]):
        is_overdue = True

    if int(assignment_due_date_string[0:4]) == int(current_datetime[0:4]):    
        if int(assignment_due_date_string[5:7]) < int(current_datetime[5:7]):
            is_overdue = True

        if int(assignment_due_date_string[5:7]) == int(current_datetime[5:7]):        
            if int(assignment_due_date_string[8:10]) < int(current_datetime[8:10]):
                is_overdue = True

            if int(assignment_due_date_string[8:10]) == int(current_datetime[8:10]):           
                if int(assignment_due_date_string[11:13]) < int(current_datetime[11:13]):
                    is_overdue = True

                if int(assignment_due_date_string[11:13]) == int(current_datetime[11:13]):               
                    if int(assignment_due_date_string[14:16]) < int(current_datetime[14:16]):
                        is_overdue = True

                    if int(assignment_due_date_string[14:16]) == int(current_datetime[14:16]):
                        if int(assignment_due_date_string[17:19]) < int(current_datetime[17:19]):
                            is_overdue = True

    return is_overdue

################################################################################

print ''

requested_user_id = 123178
user = capi.get_user(requested_user_id)
courses = capi.get_courses()
current_datetime = str(datetime.datetime.now())[:19]

print user['name'] + ' (ID: ' + str(user['id']) + ')'
print 'Email: ' + user['primary_email']
print ''

print 'See user courses? y/n'
request_courses = raw_input()
print ''

if request_courses == 'y' or request_courses == 'Y' or request_courses == 'yes' or request_courses == 'Yes':
    print 'Courses enrolled on: '
    for course in courses:
        print str(course['id']) + ': ' + course['name']
    print ''

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
                assignment_due_date = str(assignment['due_at'])
                assignment_due_date_string = assignment_due_date[0:10] + ' ' + assignment_due_date[11:19]
                is_overdue = overdue(assignment_due_date_string,current_datetime)
                if is_overdue and str(assignment['has_submitted_submissions']) == 'False':
                    print '         ' + str(assignment['id']) + ': ' + assignment['name']
                    print '             Type: ' + json.dumps(assignment['submission_types']) 
                    print '             Due at: ' + assignment_due_date_string
                    overdue_assignment_no = overdue_assignment_no + 1
        print ''
    print 'Number of overdue assignments: ' + str(overdue_assignment_no)
    print ''

'''
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
'''

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

       

