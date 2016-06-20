#!/usr/bin/env python3

# system imports
import sys


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

    def list(self, actions):
        text = ''
        for action in actions:
            if self.tasks[action]:
                text += '[%s]\n' % action
                for task in self.tasks[action]:
                    text += '%d %s\n' % (task[0], task[1])
                text += '\n'
        return text

    def add(self, action, description):
        self.tasks[action].append((self.last_index, description))
        self.last_index += 1

    def pop(self, tasknum):
        for key in self.tasks:
            for task in self.tasks[key]:
                if task[0] == tasknum:
                    description = task[1]
                    self.tasks[key].remove(task)
                    return key, description
        return None

    def parse_markdown(self):
        with open(self.filename, 'r+') as f:
            text = f.read()
            index = 1
            action = ''
            for line in text.splitlines():
                line = line.strip()
                if line == '## Add':
                    action = 'add'
                elif line == '## Fix':
                    action = 'fix'
                elif line == '## Remove':
                    action = 'rem'
                elif line == '## Change':
                    action = 'chg'
                elif line != '':
                    if action != '':
                        self.tasks[action].append((index, line[2:]))
                        index += 1
            last_index = index

    def to_markdown(self):
        text = '# ' + self.name
        def put_list(caption, action):
            t = '\n## ' + caption + '\n'
            for task in self.tasks[action]:
                t += '* ' + task[1] + '\n'
            t += '\n'
            return t
        text += put_list('Add', 'add')
        text += put_list('Fix', 'fix')
        text += put_list('Remove', 'rem')
        text += put_list('Change', 'chg')
        return text


class Version(object):
    def __init__(self, major, minor=None, patch=None):
        if minor == None and patch == None:
            s = major.split('.')
            major = int(s[0])
            minor = int(s[1])
            patch = int(s[2])
        self.major = major
        self.minor = minor
        self.patch = patch

    def increment(self):
        self.patch += 1

    def __gt__(self, v):
        if not isinstance(v, Version):
            raise NotImplementedError
        if self.major > v.major:
            return True
        if self.major == v.major and self.minor > v.minor:
            return True
        if self.major == v.major and self.minor == v.minor and self.patch > v.patch:
            return True
        return False

    def __str__(self):
        return '%d.%d.%d' % (self.major, self.minor, self.patch)


class Changelog(object):
    def __init__(self, name, filename):
        self.current_version = Version(0, 0, 1)
        self.versions = {}
        self.name = name
        self.filename = filename
        self.parse_markdown()

    def add(self, action, task):
        key = str(self.current_version)
        if not key in self.versions:
            self.versions[key] = {}
        if not action in self.versions[key]:
            self.versions[key][action] = []
        self.versions[key][action].append(task)

    def increment_version(self):
        self.current_version.increment();

    def parse_markdown(self):
        with open(self.filename, 'r') as f:
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
                    self.add(action, line[2:])

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


todolist = TaskList('TODO', 'TODO.md')
changelog = Changelog('CHANGELOG', 'CHANGELOG.md')

if sys.argv[1] in ('todo', 't'):
    if sys.argv[2] in ('list', 'ls', 'l'):
        actions = ['add', 'fix', 'rem', 'chg']
        if len(sys.argv[3:]) > 0:
            actions = sys.argv[3:]
        print(todolist.list(actions))
    elif sys.argv[2] in ('add', 'a'):
        action = None
        if sys.argv[3] in ('add', 'a'):
            action = 'add'
        elif sys.argv[3] in ('fix', 'f'):
            action = 'fix'
        elif sys.argv[3] in ('rem', 'remove', 'r'):
            action = 'rem'
        elif sys.argv[3] in ('chg', 'change', 'c'):
            action = 'chg'
        if action:
            todolist.add(action, sys.argv[4])
        else:
            raise ValueError
elif sys.argv[1] in ('do', 'd'):
    try:
        index = int(sys.argv[2])
        print('removing index', index)
        action, task = todolist.pop(index)
        print(action, task)
        changelog.add(action, task)
    except:
        raise ValueError
elif sys.argv[1] in ('version', 'ver', 'v'):
    changelog.increment_version()
elif sys.argv[1] in ('remove', 'rem', 'r'):
    try:
        index = int(sys.argv[2])
        todolist.pop(index)
    except:
        raise ValueError
elif sys.argv[1] in ('help', 'h'):
    pass

with open('CHANGELOG.md', 'w+') as f:
    f.write(changelog.to_markdown())

with open('TODO.md', 'w+') as f:
    f.write(todolist.to_markdown())
