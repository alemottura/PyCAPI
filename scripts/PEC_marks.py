#!/usr/bin/python

# This script lists all courses in a Canvas account, and published/unpublished assignments within each

import PyCAPI
import csv

capi = PyCAPI.CanvasAPI()




with open('./PECgrades.csv', 'rb') as csvfile:
	content = csv.reader(csvfile, delimiter=',', quotechar='"')
	for student in content:
		user_id = student[1]
		grade = student[6]
		
		comment = "Here is the breakdown for each individual question (with comments/feedback):\n"
		comment += "Q1a: " + student[7] + "/3 - " + student[8] + "\n"
		comment += "Q1b: " + student[9] + "/5 - " + student[10] + "\n"
		comment += "Q1c: " + student[11] + "/2 - " + student[12] + "\n"
		comment += "Q2a: " + student[13] + "/3 - " + student[14] + "\n"
		comment += "Q2b: " + student[15] + "/3 - " + student[16] + "\n"
		comment += "Q2c: " + student[17] + "/3 - " + student[18] + "\n"
		comment += "Q2d: " + student[19] + "/6 - " + student[20] + "\n"
		comment += "Q2e: " + student[21] + "/2 - " + student[22] + "\n"
		comment += "Q2f: " + student[23] + "/3 - " + student[24] + "\n"
		comment += "Q3a: " + student[25] + "/5 - " + student[26] + "\n"
		comment += "Q3b: " + student[27] + "/5 - " + student[28] + "\n"
		comment += "Q3c: " + student[29] + "/5 - " + student[30] + "\n"
		comment += "Q3d: " + student[31] + "/5 - " + student[32] + "\n"
		comment += "Q4a: " + student[33] + "/2 - " + student[34] + "\n"
		comment += "Q4b: " + student[35] + "/3 - " + student[36] + "\n"
		comment += "Q4c: " + student[37] + "/5 - " + student[38] + "\n"
		comment += "Q4d: " + student[39] + "/5 - " + student[40] + "\n"
		comment += "Q5a: " + student[41] + "/5 - " + student[42] + "\n"
		comment += "Q5b: " + student[43] + "/5 - " + student[44] + "\n"
		comment += "Q6: " + student[45] + "/5 - " + student[46] + "\n"
		comment += "Q7a: " + student[47] + "/4 - " + student[48] + "\n"
		comment += "Q7b: " + student[49] + "/6 - " + student[50] + "\n"
		comment += "Q7c: " + student[51] + "/10 - " + student[52] + "\n"
		print user_id
		print grade
		print comment

		capi.comment_assignment_submission(22577, 82767, user_id, comment)

