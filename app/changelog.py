from .util import *
from .version import Version

import os


class Changelog(object):
	def __init__(self, name, filename):
		self.current_version = Version(0, 0, 1)
		self.versions = {}
		self.name = name
		self.filename = filename
		self.parse_markdown()

	def add(self, action, task, version=None):
		if not version:
			version = self.current_version
		key = str(version)
		if not key in self.versions:
			self.versions[key] = {}
		if not action in self.versions[key]:
			self.versions[key][action] = []
		self.versions[key][action].append(task)

	def set_version(self, version):
		self.current_version = version

	def increment_version(self):
		self.current_version.increment()
		self.versions[str(self.current_version)] = {}

	def parse_markdown(self):
		if os.path.exists(self.filename):
			with open(self.filename, 'r+') as f:
				text = f.read()
				version = Version(0, 0, 1)
				action = ''
				for line in text.splitlines():
					if line[:3] == '## ':
						version = Version(line[3:])
						self.versions[str(version)] = {}
						if version > self.current_version:
							self.current_version = version
					elif line[:4] == '### ':
						action = line[4:].lower()
					elif line[:2] == '* ':
						self.add(action, line[2:], version)

	def to_markdown(self):
		text = '# ' + self.name
		for version in self.versions:
			text += '\n## %s' % str(version)
			for action in self.versions[str(version)]:
				text += '\n### %s\n' % action
				for task in self.versions[str(version)][action]:
					text += '* %s\n' % task
			text += '\n'
		return text

