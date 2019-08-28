#
#       make_meqs.py
#
#       This code will create module evaluation questionnaires in each
#		Canvas course.
#
#       Things that need to be set:
#
#       input_file - path of Excel file containing course information
input_file = '/mnt/metadmin/CANVASBOTS/UG/Courses_and_Assignments/input_file.xlsx'
#
#
import sys
sys.path.append("../module/") # First two lines are needed for import of PyCAPI
import PyCAPI
import uob_utils
import datetime
import json
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import colors
from openpyxl.styles import Font, Color, PatternFill
from openpyxl import worksheet
import re


capi = PyCAPI.CanvasAPI()


###############################################################################
# Read in excel file with courses/module information
#


SX = 'S1'
semester = 'Semester 1'
available_date = datetime.datetime(2019, 1, 1, 00, 00)
due_date = datetime.datetime(2019, 12, 20, 23, 59)
lock_date = datetime.datetime(2019, 12, 31, 23, 59)
courses = [{'id': 24191, 'title': 'LI Physical Materials Science', 'code': 'LI PMS', 'lecturers': ['Alessandro Mottura']}]

###############################################################################
# Create module evaluation questionnaires in each course
#
for course in courses:
	quiz_data = {
		'quiz[title]': 'MEQ - ' + SX + ' - ' + course['code'],
		'quiz[description]': 'This is the ' + semester + ' module evaluation questionnaire (MEQ) for the ' + course['title'] + ' module. Please complete this by the deadline.',
		'quiz[quiz_type]': 'survey',
		'quiz[shuffle_answers]': 0,
		'quiz[hide_results]': 'always',
		'quiz[show_correct_answers]': 0,
		'quiz[allowed_attempts]': 1,
		'quiz[one_question_at_a_time]': 0,
		'quiz[anonymous_submissions]': 1,
		'quiz[unlock_at]': available_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
		'quiz[due_at]': due_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
		'quiz[lock_at]': lock_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
	}

	quiz = capi.post('/courses/%s/quizzes' % course['id'], payload=quiz_data)
	
	multiple_choice_question_data = {
		'question[question_name]': 'Question',
		'question[question_text]': 'This is the question text',
		'question[question_type]': 'multiple_choice_question',
		'question[points_possible]': 0,
		'question[answers][0][answer_text]': 'Strongly agree',
		'question[answers][0][answer_weight]': 0,
		'question[answers][1][answer_text]': 'Agree',
		'question[answers][1][answer_weight]': 0,
		'question[answers][2][answer_text]': 'Neutral',
		'question[answers][2][answer_weight]': 0,
		'question[answers][3][answer_text]': 'Disagree',
		'question[answers][3][answer_weight]': 0,
		'question[answers][4][answer_text]': 'Strongly disagree',
		'question[answers][4][answer_weight]': 0
	}
	
	essay_question_data = {
		'question[question_name]': 'Question',
		'question[question_text]': 'This is the question text',
		'question[question_type]': 'essay_question',
		'question[points_possible]': 0
	}
	
	essay_question_data = {
		'question[question_name]': 'Question',
		'question[question_text]': 'This is the question text',
		'question[question_type]': 'essay_question',
		'question[points_possible]': 0
	}
	
	test_question_data = {
		'question[question_name]': 'Question',
		'question[question_text]': 'This is the question text',
		'question[question_type]': 'short_answer_question',
		'question[points_possible]': 0
	}
	
	for lecturer in course['lecturers']:
		multiple_choice_question_data['question[question_text]'] = lecturer + ' is good at explaining things'
		question = capi.post('/courses/%s/quizzes/%s/questions' % (course['id'],quiz['id']), payload=multiple_choice_question_data)
		
		multiple_choice_question_data['question[question_text]'] = lecturer + ' has made the subject interesting'
		question = capi.post('/courses/%s/quizzes/%s/questions' % (course['id'],quiz['id']), payload=multiple_choice_question_data)
		
		essay_question_data['question[question_text]'] = 'What aspects of ' + lecturer + '\'s approach to teaching best helped your learning?'
		question = capi.post('/courses/%s/quizzes/%s/questions' % (course['id'],quiz['id']), payload=essay_question_data)
		
		essay_question_data['question[question_text]'] = 'What could ' + lecturer + ' have done differently to hel you learn more effectively?'
		question = capi.post('/courses/%s/quizzes/%s/questions' % (course['id'],quiz['id']), payload=essay_question_data)
	
	
	multiple_choice_question_data['question[question_text]'] = 'The criteria used in marking have been made clear in advance'
	question = capi.post('/courses/%s/quizzes/%s/questions' % (course['id'],quiz['id']), payload=multiple_choice_question_data)
	
	multiple_choice_question_data['question[question_text]'] = 'Feedback on my work has been timely (within 3 working weeks)'
	question = capi.post('/courses/%s/quizzes/%s/questions' % (course['id'],quiz['id']), payload=multiple_choice_question_data)
	
	multiple_choice_question_data['question[question_text]'] = 'I received helpful comments on my work'
	question = capi.post('/courses/%s/quizzes/%s/questions' % (course['id'],quiz['id']), payload=multiple_choice_question_data)
	
	essay_question_data['question[question_text]'] = 'Are there any particular assessments you would like to comment on? What went well, and what could be improved?'
	question = capi.post('/courses/%s/quizzes/%s/questions' % (course['id'],quiz['id']), payload=essay_question_data)
	
	multiple_choice_question_data['question[question_text]'] = 'Learning materials (e.g. lecture recordings, lecture notes, web links, quizzes, resource lists etc.) made available in this module have enhanced my learning'
	question = capi.post('/courses/%s/quizzes/%s/questions' % (course['id'],quiz['id']), payload=multiple_choice_question_data)
	
	multiple_choice_question_data['question[question_text]'] = 'The module is well organised and running smoothly'
	question = capi.post('/courses/%s/quizzes/%s/questions' % (course['id'],quiz['id']), payload=multiple_choice_question_data)
	
	multiple_choice_question_data['question[question_text]'] = 'Overall, are you satisfied with this module?'
	question = capi.post('/courses/%s/quizzes/%s/questions' % (course['id'],quiz['id']), payload=multiple_choice_question_data)
	
	essay_question_data['question[question_text]'] = 'Please provide any comments you would wish to make'
	question = capi.post('/courses/%s/quizzes/%s/questions' % (course['id'],quiz['id']), payload=essay_question_data)
		
	quiz_data = {
		'quiz[published]': 1
	}
	quiz = capi.put('/courses/%s/quizzes/%s' % (course['id'],quiz['id']), payload=quiz_data)
	
	
	#quiz_id = 65867
	
	#result = capi.get('/courses/%s/quizzes/%s/questions' % (course['id'], quiz_id))
	#print result





