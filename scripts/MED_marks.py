#!/opt/local/bin/python

# This script lists all courses in a Canvas account, and published/unpublished assignments within each

import PyCAPI
import csv

capi = PyCAPI.CanvasAPI()




with open('./MED_marks.csv', 'rU') as csvfile:
	content = csv.reader(csvfile, delimiter=',', quotechar='"')
	for student in content:
		user_id = student[1]
		grade = student[6]
		
		comment = "I have noticed that the mark for the presentation is not included here.\n"
		comment += "Report: " + student[4] + "/100" + "\n"
		comment += "Presentation: " + student[5] + "/100" + "\n"
		comment += "Total: " + student[6] + "/100" + "\n"
		comment += "The presentation is weighted at 30% of the total, the report is 70%.\n"


		print student[0]
		print user_id
		print grade
		print comment
		print ''

		#capi.comment_assignment_submission(28638, 104449, user_id, comment)
		capi.grade_assignment_submission(26914, 96088, user_id, grade, comment)

