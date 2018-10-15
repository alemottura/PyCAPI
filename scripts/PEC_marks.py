#!/opt/local/bin/python

# This script lists all courses in a Canvas account, and published/unpublished assignments within each

import PyCAPI
import csv

capi = PyCAPI.CanvasAPI()




with open('./PEC_marks.csv', 'rU') as csvfile:
	content = csv.reader(csvfile, delimiter='\t', quotechar='"')
	for student in content:
		user_id = student[1]
		grade = student[45]
		
		comment = "Here is the breakdown for each individual question (with comments/feedback):\n"
		comment += "Q1a: " + student[7] + "/7 - " + student[8] + "\n"
		comment += "Q1b: " + student[9] + "/3 - " + student[10] + "\n"
		comment += "Q1c: " + student[11] + "/2 - " + student[12] + "\n"
		comment += "Q1d: " + student[13] + "/3 - " + student[14] + "\n"
		comment += "Q1e: " + student[15] + "/5 - " + student[16] + "\n"
		
		comment += "Q2a: " + student[17] + "/6 - " + student[18] + "\n"
		comment += "Q2b: " + student[19] + "/10 - " + student[20] + "\n"
		comment += "Q2c: " + student[21] + "/4 - " + student[22] + "\n"

		comment += "Q3: " + student[23] + "/10 - " + student[24] + "\n"

		comment += "Q4a: " + student[25] + "/4 - " + student[26] + "\n"
		comment += "Q4b: " + student[27] + "/4 - " + student[28] + "\n"
		comment += "Q4c: " + student[29] + "/6 - " + student[30] + "\n"
		comment += "Q4d: " + student[31] + "/6 - " + student[32] + "\n"
		
		comment += "Q5a: " + student[33] + "/3 - " + student[34] + "\n"
		comment += "Q5b: " + student[35] + "/9 - " + student[36] + "\n"
		comment += "Q5c: " + student[37] + "/3 - " + student[38] + "\n"
		comment += "Q5d: " + student[39] + "/5 - " + student[40] + "\n"
		
		
		comment += "Q6a: " + student[41] + "/6 - " + student[42] + "\n"
		comment += "Q6b: " + student[43] + "/4 - " + student[44] + "\n"

		print student[0]
		print user_id
		print grade
		print comment
		print ''

		#capi.comment_assignment_submission(28638, 104449, user_id, comment)
		capi.grade_assignment_submission(28638, 104449, user_id, grade)

