

included_terms = ['2018/19']

import PyCAPI
import datetime
import uob_utils

capi = PyCAPI.CanvasAPI()


# get all account courses
allcourses = capi.get_courses(account_id='114', include=['term','teachers'])

courses = []

#for course in allcourses:
#	if course['term']['name'] in included_terms:
#		courses.append(course)


for course in allcourses:
	if course['id'] == 34797:
		courses.append(course)

for course in courses:
	print " "
	print('%s: %s (term: %s, account: %s)' % (course['id'], course['name'], course['term']['name'], course['account_id']))
	assignments = capi.get_assignments(course['id'])
	for assignment in assignments:
		if assignment['due_at'] == None:
			print ('  -- - %s: %s (null)' % (assignment['id'], assignment['name']))
		else:
			if uob_utils.AcademicYear(datetime.datetime.strptime(assignment['due_at'], "%Y-%m-%dT%H:%M:%SZ").date()) == 2019:
				print ('  ok - %s: %s (%s - %s - %s)' % (assignment['id'], assignment['name'], assignment['unlock_at'], assignment['due_at'], assignment['lock_at']))
			else:
				proposed_due_date = uob_utils.FindCorrespondingDate(datetime.datetime.strptime(assignment['due_at'], "%Y-%m-%dT%H:%M:%SZ").date(),2018)
				proposed_due_datetime = datetime.datetime.strptime(str(proposed_due_date)+' 09:00:00', "%Y-%m-%d %H:%M:%S")
				proposed_due_datetime = datetime.datetime(2019, 2, 1, 12, 00)
				print ('  %s: %s (%s) -> (%s)' % (assignment['id'], assignment['name'], str(datetime.datetime.strptime(assignment['due_at'], "%Y-%m-%dT%H:%M:%SZ")), str(proposed_due_datetime)))
				change = raw_input ('      Do you want to change the due date as above? (y/n): ')
				if change == 'y':
					if assignment['lock_at'] != None:
						proposed_lock_date = uob_utils.FindCorrespondingDate(datetime.datetime.strptime(assignment['lock_at'], "%Y-%m-%dT%H:%M:%SZ").date(),2018)
						proposed_lock_datetime = datetime.datetime.strptime(str(proposed_lock_date)+' 23:59:59', "%Y-%m-%d %H:%M:%S")
						proposed_lock_datetime = datetime.datetime(2019, 2, 15, 12, 00)
						capi.update_assignment(course['id'], assignment['id'], 'lock_at', proposed_lock_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"))
						
					capi.update_assignment(course['id'], assignment['id'], 'due_at', proposed_due_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"))
						
					#if assignment['unlock_at'] != None:
					#	proposed_unlock_date = uob_utils.FindCorrespondingDate(datetime.datetime.strptime(assignment['unlock_at'], "%Y-%m-%dT%H:%M:%SZ").date(),2018)
					#	proposed_unlock_datetime = datetime.datetime.strptime(str(proposed_unlock_date)+' 00:00:00', "%Y-%m-%d %H:%M:%S")
					#	capi.update_assignment(course['id'], assignment['id'], 'unlock_at', proposed_unlock_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"))
					
					
					


