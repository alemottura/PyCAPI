

import PyCAPI

capi = PyCAPI.CanvasAPI()

#capi.conclude_course('1271')


# get all account courses
courses = capi.get_account_courses('114', include='term', state='available')

# for every course in account courses
for course in courses:
	if course['term']['name'] == '2015/16':
		print " "
		print('%s: %s (term: %s, account: %s)' % (course['id'], course['name'], course['term']['name'], course['account_id']))
		decision = raw_input('   Do you want to conclude this course [y/n]? ')
		if decision == 'y':
			capi.conclude_course(course['id'])
			print '   This course has been concluded.'
		#print course
#	
	# if course is NOT in PGT sub-account
#	if course['account_id'] != 120:
#		
		# check whether course includes Andrea as teacher
#		if any(teacher['id'] == 1063 for teacher in course['teachers']):
#			
			# print some details about the course
#			print " "
#			print('%s: %s (term: %s, account: %s)' % (course['id'], course['name'], course['term']['name'], course['account_id']))
#			decision = raw_input('   Do you want to move course to PGT sub-account (120) [y/n]? ')
#			if decision == 'y':
#				capi.update_course(course['id'], 'account_id', 120)
#				print '   This course has been moved to PGT sub-account.'

		
#capi.update_course('24191','account_id',121)


