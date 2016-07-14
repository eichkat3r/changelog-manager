import os

from .util import *


class TaskList(object):
	def __init__(self, name, filename):
		self.tasks = {
			'add': [],
			'fix': [],
			'rem': [],
			'chg': []
		}
		self.name = name
		self.filename = filename
		self.last_index = 1
		self.parse_markdown()

	"""
	@param actions action categories to show in list
	@return colored list as a string
	"""
	def list(self, actions):
		text = ''
		for action in actions:
			if self.tasks[action]:
				# action caption
				text += '%s[%s]%s\n' % (COLOR_RED, action, COLOR_END)
				# list of tasks for each action
				for task in self.tasks[action]:
					text += '%s%d%s %s\n' % (COLOR_BLUE, task[0], COLOR_END, task[1])
				text += '\n'
		return text

	"""
	@param action task action
	@param description task description
	"""
	def add(self, action, description):
		self.tasks[action].append((self.last_index, description))
		self.last_index += 1

	"""
	@param tasknum task index, can be seen in list
	@return action and task description or None
	"""
	def pop(self, tasknum):
		for key in self.tasks:
			for task in self.tasks[key]:
				if task[0] == tasknum:
					description = task[1]
					self.tasks[key].remove(task)
					return key, description
		return None

	"""
	"""
	def parse_markdown(self):
		if not os.path.exists(self.filename):
			with open(self.filename, 'w+') as f:
				pass
			return
		with open(self.filename, 'r+') as f:
			text = f.read()
			index = 1
			action = ''
			for line in text.splitlines():
				line = line.strip()
				if line[:3] == '## ':
					action = short_action_names[line[3:]]
				elif line[:2] == '* ':
					if action != '':
						self.tasks[action].append((index, line[2:]))
						index += 1
			last_index = index

	"""
	@return markdown representation as a string
	"""
	def to_markdown(self):
		text = '# ' + self.name
		def put_list(caption, action):
			t = '\n## ' + caption + '\n'
			for task in self.tasks[action]:
				t += '* ' + task[1] + '\n'
			t += '\n'
			return t
		for action in ['add', 'fix', 'rem', 'chg']:
			text += put_list(long_action_names[action], action)
		return text

