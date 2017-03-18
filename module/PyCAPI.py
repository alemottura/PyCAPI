
import itertools
import requests
import os

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

	def post(self, api_url, payload=None):
		url = self.api_url + api_url # compose url for post request
		if payload is None: # if no payload, send empty payload
			payload = {}
		r = self.session.post(url, data=payload) # send post request with data
		r.raise_for_status() # raise an exception if there is an http error
		return r # return result of request

	def get(self, api, to_json=True, payload=None, single=False):
		url = self.api_url + api # compose url for the initial get request
		responses = [] # prepare list to collate responses
		while True: # enter infinite loop
			if payload is None: # if no payload, send empty payload
				payload = {}
			r = self.session.get(url, data=payload) # send get request
			r.raise_for_status() # raise an exception if there is an http error
			responses.append(r) # append result of request to responses
			if 'next' in r.links: # if the result shows there is more data to obtain
				url = r.links['next']['url'] # obtain url for the next chunk of data, and start at the top of while loop
			else: # if there is no more data to obtain, then break the infinite loop
				break
		if to_json: # if response is in json format, process it accordingly
			responses = [r.json() for r in responses]
		if single: # if request is meant to have returned a single item, just return the item
			return responses[0]
		else: # return the full list if it contains more than a single item
			return list(reduce(lambda x, y: itertools.chain(x, y), responses))


	def get_user(self, user_id):
		"""Obtains the profile of a user."""
		return self.get('/users/%s/profile' % user_id, single=True)

	def get_course_groups(self, course_id):
		"""Obtains groups within a course."""
		return self.get('/courses/%s/groups' % course_id)

	def get_group_membership(self, group_id):
		"""Obtains membership of a group."""
		return self.get('/groups/%s/memberships' % group_id)

	def get_courses(self):
		"""Obtain list of courses for the authorised user."""
		return self.get('/courses')

	def get_account_courses(self, account_id):
		"""Obtain list of course for a specific account or sub-account."""
		return self.get('/accounts/%s/courses' % account_id)

	def get_assignments(self, course_id):
		"""Obtain assignments in a specific course."""
		return self.get('/courses/%s/assignments' % course_id)

	def get_users(self, course_id):
		"""Obtain users in a specific course."""
		return self.get('/courses/%s/users' % course_id)

	def get_user_activity_summary(self):
		"""Obtain summary of users activity - Sam"""
		return self.get('/users/self/activity_stream/summary')

	def get_user_submission_details(self, course_id, assignment_id):
		"""Obtain details about a user submissions - Sam"""
		"""This function currently doesn't work as running it does not retrieve information"""
		return self.get('/courses/%s/assignments/%s/submissions' % (course_id, assignment_id))

	def get_quiz_submissions(self, course_id, quiz_id):
		"""Obtain submissions of a quiz."""
		return self.get('/courses/%s/quizzes/%s/submissions' % (course_id, quiz_id))

	def get_assignment_submissions(self, course_id, assignment_id, grouped=False):
		"""Need to figure out what this function does..."""
		payload = {'grouped': grouped}
		submissions = self.get('/courses/%s/assignments/%s/submissions' % (course_id, assignment_id), payload=payload)        
		return filter(lambda sub: sub['workflow_state'] != 'unsubmitted', submissions)

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

	def set_group_name(self, group_id, name):
		"""Set name of a group."""
		payload = {'name': name}
		return self.put('/groups/%s' % (group_id), payload=payload)            

	def set_group_membership(self, group_set_builder):
		results = []
		for group_id, membership in group_set_builder.groups.iteritems():            
			payload = {}
			payload['members[]'] = membership
			self.put('/groups/%s' % (group_id), payload=payload)

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

	def custom_get(self,custom_url):
		return self.get(custom_url)



