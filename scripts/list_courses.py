#!/usr/bin/python

# This script lists all courses in a Canvas account, and published/unpublished assignments within each

import PyCAPI

capi = PyCAPI.CanvasAPI()

courses = capi.get_account_courses('115')

for course in courses:
	if int(course['enrollment_term_id']) == 74:
		print " "
		print('%s: %s (%s)' % (course['id'], course['name'], course['enrollment_term_id']))
		assignments = capi.get_assignments(course['id'])
		print "  Published assignments:"
		for assignment in assignments:
			if assignment['published']:
				if 'online_quiz' in assignment['submission_types']:
					print('    %s: %s (%s, quiz_id: %s, locked: %s)' % (assignment['id'], assignment['name'], assignment['submission_types'], assignment['quiz_id'], assignment['locked_for_user']))
				else:
					print('    %s: %s (%s, locked: %s)' % (assignment['id'], assignment['name'], assignment['submission_types'], assignment['locked_for_user']))
		print "  Unpublished assignments:"
		for assignment in assignments:
			if not assignment['published']:
				if 'online_quiz' in assignment['submission_types']:
					print('    %s: %s (%s, quiz_id: %s, locked: %s)' % (assignment['id'], assignment['name'], assignment['submission_types'], assignment['quiz_id'], assignment['locked_for_user']))
				else:
					print('    %s: %s (%s, locked: %s)' % (assignment['id'], assignment['name'], assignment['submission_types'], assignment['locked_for_user']))






#assignments = capi.get_assignments('22417')

#for assignment in assignments:
#	print " ", assignment['id'], assignment['name'], assignment
