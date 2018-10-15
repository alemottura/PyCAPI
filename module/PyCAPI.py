
import itertools
import requests
import os
from time import sleep

class CanvasAPI():
	""""""
	
	def __init__(self, access_token=None, base_url='https://canvas.bham.ac.uk', api_prefix='/api/v1', path_to_access_token='~/.canvastoken'):
		"""
		You can use the CanvasAPI() class to construct an object that accesses the API functions.
		No input is required when constructing the object, provided you have a Canvas token stored in a file (.canvastoken) in your home directory.
		"""
		self.api_url = base_url + api_prefix # compose base url for Canvas API
		if access_token == None: # if there is no access token when constructing the object, look for .canvastoken file
			if not os.path.isfile(os.path.expanduser(path_to_access_token)):
				raise RuntimeError('Provide a Canvas token in ~/.canvastoken or as an argument of the call.')
			if int(oct(os.stat(os.path.expanduser(path_to_access_token)).st_mode)[-3:]) > 600: # check that .canvastoken file has appropriate file restrictions
				raise RuntimeError('Permissions of Canvas token are not secure enough.')
			with open(os.path.expanduser(path_to_access_token)) as f: # read Canvas token from .canvastoken file
				access_token = f.read().strip()
		self.session = requests.Session() # start an HTTP session
		self.session.headers = {'Authorization': 'Bearer %s' % access_token} # pass the Canvas token in the HTTP headers

	def put(self, api_url, payload=None):
		url = self.api_url + api_url # compose url for put request
		if payload is None: # if no payload, send empty payload
			payload = {}
		r = self.session.put(url, params=payload) # send put request with data
		r.raise_for_status() # raise an exception if there is an http error
		return r # return result of request

	def post(self, api_url, to_json=True, payload=None):
		url = self.api_url + api_url # compose url for post request
		if payload is None: # if no payload, send empty payload
			payload = {}
		r = self.session.post(url, data=payload) # send post request with data
		r.raise_for_status() # raise an exception if there is an http error
		if to_json:
			r = r.json()
		return r # return result of request

	def post_file(self,url, to_json=True, payload=None):
		if payload is None: # if no payload, send empty payload
			payload = {}
		r = requests.post(url, files=payload) # post to url including multi-part data
		r.raise_for_status() # raise an exception if there is an http error
		if to_json:
			r = r.json()
		return r # return result of request

	def get(self, api, to_json=True, payload=None, single=False, first_page_only=False):
		url = self.api_url + api # compose url for the initial get request
		responses = [] # prepare list to collate responses
		while True: # enter infinite loop
			if payload is None: # if no payload, send empty payload
				payload = {}
			attempt = 0 # set up request attempt counter
			try_again = True # set up request attempt boolean
			while try_again == True: # while try_again is equal to two
				attempt += 1 # increment attempt counter
				r = self.session.get(url, data=payload) # send get request
				if 200 <= r.status_code <= 299: # if request is OK...
					try_again = False # ...do not repeat request - move on...
				elif 500 <= r.status_code <= 599: # if request indicates server error...
					if attempt < 5: # ...and we have repeated the request less than 5 times...
						try_again = True # ...try request again
						sleep(5) # wait 5s before attempting again
					else: # ...if request has been repeated 5 times or more...
						try_again = False # ...do not repeat request
						r.raise_for_status() # raise error
				else: # otherwise (all other status codes)
					try_again = False # do not repeat request
					r.raise_for_status() # raise error
			#r = self.session.get(url, data=payload) # send get request
			r.raise_for_status() # this is really not needed - it is here in case something went wrong...
			responses.append(r) # append result of request to responses
			if 'next' in r.links: # if the result shows there is more data to obtain
				url = r.links['next']['url'] # obtain url for the next chunk of data, and start at the top of while loop
			else: # if there is no more data to obtain, then break the infinite loop
				break
			if first_page_only:
				break
		if to_json: # if response is in json format, process it accordingly
			responses = [r.json() for r in responses]
		if single: # if request is meant to have returned a single item, just return the item
			return responses[0]
		else: # return the full list if it contains more than a single item
			return list(reduce(lambda x, y: itertools.chain(x, y), responses))

	def delete(self, api_url, payload=None):
		url = self.api_url + api_url # compose url for delete request
		if payload is None: # if no payload, send empty payload
			payload = {}
		r = self.session.delete(url, data=payload) # send delete request with data
		r.raise_for_status() # raise an exception if there is an http error
		return r # return result of request







	# USER-RELATED FUNCTIONS
	def get_user(self, user_id):
		"""Obtains the profile of a user."""
		return self.get('/users/%s/profile' % user_id, single=True)

	def get_users(self, course_id):
		"""Obtain users in a specific course."""
		return self.get('/courses/%s/users' % course_id)

	def get_course_groups(self, course_id):
		"""Obtains groups within a course."""
		return self.get('/courses/%s/groups' % course_id)

	def get_group_membership(self, group_id):
		"""Obtains membership of a group."""
		return self.get('/groups/%s/memberships' % group_id)
	
	def set_group_name(self, group_id, name):
		"""Set name of a group."""
		payload = {'name': name}
		return self.put('/groups/%s' % (group_id), payload=payload)
	
	def set_group_membership(self, group_set_builder):
		"""Add members to a group."""
		results = []
		for group_id, membership in group_set_builder.groups.iteritems():            
			payload = {}
			payload['members[]'] = membership
			self.put('/groups/%s' % (group_id), payload=payload)

	def get_user_activity_summary(self):
		"""Obtain summary of users activity"""
		return self.get('/users/self/activity_stream/summary')





	

	# COURSE-RELATED FUNCTIONS
	def get_courses(self, course_id=None, user_id=None, account_id=None, include=None, state=None):
		"""
		Obtain course details.
		  - If course_id is set, then this returns details for the requested course
		  - If account_id is set, then this returns details of all courses in the account (if you have necessary account permissions)
		  - If none of these are set, then this returns details of all courses the user is enrolled in
		  - Include is an optional list of strings which can include values such as:
		       'term', 'teachers', 'needs_grading_count', etc.
		    in order to obtain more information from the course
		  - State is an optional list of strings which can be used to request only courses that match the requested state such as:
		       'ubpublished', 'available', 'completed' and 'deleted'
		"""
		payload = {}
		if include != None:
			payload['include[]'] = include
		if state != None:
			payload['state[]'] = state
		if account_id != None:
			return self.get('/accounts/%s/courses' % account_id, payload=payload)
		elif course_id != None:
			return self.get('/courses/%s' % course_id, single=True, payload=payload)
		elif user_id != None:
			return self.get('users/%s/courses' % user_id, payload=payload)
		else:
			return self.get('/courses', payload=payload)

	def update_course(self, course_id, parameter, value):
		"""Update course details for a specific course. See online documentation for allowed parameters."""
		payload = {'course[%s]' % parameter: value}
		return self.put('/courses/%s' % course_id, payload=payload)
		
	def conclude_course(self, course_id):
		"""Conclude a course."""
		payload = {'event':'conclude'}
		return self.delete('/courses/%s' % course_id, payload=payload)

	def delete_course(self, course_id):
		"""Conclude a course."""
		payload = {'event':'delete'}
		return self.delete('/courses/%s' % course_id, payload=payload)

	def upload_course_file(self, course_id, file_name, file_path='/'):
		"""Upload file to course files."""
		payload = {}
		payload['name'] = file_name
		payload['parent_folder_path'] = file_path
		pending_object = self.post('/courses/%s/files' % course_id, payload=payload) # Make post request to Canvas to create pending object
		payload = list(pending_object['upload_params'].items())
		with open(file_name, 'rb') as f:
			file_content = f.read() # Add file content to payload returned by previous post request
		payload.append((u'file', file_content))
		return self.post_file(pending_object['upload_url'], payload=payload) # Post the new payload to the url provided by the previous post request






	# ASSIGNMENT-RELATED FUNCTIONS
	def get_assignment(self, course_id, assignment_ids):
		"""Obtain a specific assignment in a specific course."""
		return self.get('/courses/%s/assignments/%s' % (course_id, assignment_ids), single=True)
	
	def get_assignments(self, course_id):
		"""Obtain assignments in a specific course."""
		return self.get('/courses/%s/assignments' % course_id)

	def get_assignment_submissions(self,course_id, assignment_ids='', user_ids='all', grouped=True):
		"""
		Returns details of assignment submissions in a particular course.
		  - Assignment_ids can be left blank, or changed to be a string (or list of strings) to obtain submissions to particular assignments
		  - User_ids can be left as 'all', or changed to be a string (or a list of strings) to obtain submissions for specific students
		  - The grouped flag returns submissions grouped by user_id if true
		"""
		payload = {}
		payload['student_ids[]'] = user_ids # by default ('all'), this returns all submissions for all students
		payload['assignment_ids[]'] = assignment_ids # by default (if blank), this returns submissions for all assignments
		payload['grouped'] = grouped # this groups all submissions by user, if true
		return self.get('/courses/%s/students/submissions' % course_id, payload=payload)

	def get_quiz_submissions(self, course_id, quiz_id):
		"""Obtain submissions of a quiz."""
		return self.get('/courses/%s/quizzes/%s/submissions' % (course_id, quiz_id))
	
	def grade_assignment_submission(self, course_id, assignment_id, user_id, grade, comment=None):
		"""Grade assignment submission and add comments if necessary."""
		payload = {'grade_data[%s][posted_grade]' % user_id: grade}
		if comment is not None:
			payload['grade_data[%s][text_comment]' % user_id] = comment
		return self.post('/courses/%s/assignments/%s/submissions/update_grades' % (course_id, assignment_id), payload=payload)            

	def comment_assignment_submission(self, course_id, assignment_id, user_id, comment):
		"""Add comment to assignment submission."""
		payload = {'grade_data[%s][text_comment]' % user_id: comment}
		return self.post('/courses/%s/assignments/%s/submissions/update_grades' % (course_id, assignment_id), payload=payload)
	
	def comment_assignment_submission_with_upload(self, course_id, assignment_id, user_id, file_name):
		"""Attach document as comment to assignment submission."""
		payload = {}
		payload['name'] = file_name
		pending_object = self.post('/courses/%s/assignments/%s/submissions/%s/comments/files' % (course_id, assignment_id, user_id), payload=payload) # Make post request to Canvas to create pending object
		payload = list(pending_object['upload_params'].items())
		with open(file_name, 'rb') as f:
			file_content = f.read() # Add file content to payload returned by previous post request
		payload.append((u'file', file_content))
		pending_file = self.post_file(pending_object['upload_url'], payload=payload) # Post the new payload to the url provided by the previous post request
		payload = {}
		payload = {'grade_data[%s][text_comment]' % user_id: 'See attached file'}
		payload = {'grade_data[%s][file_ids]' % user_id: [pending_file['id']]}
		return self.post('/courses/%s/assignments/%s/submissions/update_grades' % (course_id, assignment_id), payload=payload)
		

	def get_submission_attachments(self, submission, as_bytes=False):
		"""
		Get a dictionary containing the attachment files for this submission.
		:param submission: A JSON submission object.
		:param as_bytes: If True, get the file as bytes, else it will be returned as text.
		:return: A dictionary mapping filename to file contents.
		"""
		attachments = {}
		if 'attachments' in submission:
			for attachment in submission['attachments']:
				r = requests.get(attachment['url'], params={'access_token': self.access_token})
				if as_bytes:
					attachments[attachment['filename']] = r.content
				else:
					attachments[attachment['filename']] = r.text
		return attachments

	def upload_file_to_assignment(self, course_id, assignment_id, user_id, file_name):
		"""Upload file to assignment. This only works if you are Admin."""
		pending_object = self.post('/courses/%s/assignments/%s/submissions/%s/files?as_user_id=%s' % (course_id, assignment_id, user_id, user_id)) # Make post request to Canvas to create pending object
		payload = list(pending_object['upload_params'].items())
		with open(filename, 'rb') as f:
			file_content = f.read() # Add file content to payload returned by previous post request
		payload.append((u'file', file_content))
		return self.post_file(pending_object['upload_url'], payload=payload) # Post the new payload to the url provided by the previous post request

	def update_assignment(self, course_id, assignment_id, parameter, value):
		"""Update assignment details for a specific assignment. See online documentation for allowed parameters."""
		payload = {'assignment[%s]' % parameter: value}
		return self.put('/courses/%s/assignments/%s' % (course_id, assignment_id), payload=payload)
	

def datetime2unicode(datetimevar):
	datetimevar = list(str(datetimevar))
	datetimevar[10] = 'T'
	datetimevar.append('Z')
	datetimevar = unicode(''.join(datetimevar))
	return datetimevar
