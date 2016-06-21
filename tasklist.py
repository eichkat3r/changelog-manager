from util import *

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
                text += '%s[%s]%s\n' % (COLOR_RED, action, COLOR_END)
                for task in self.tasks[action]:
                    text += '%s%d%s %s\n' % (COLOR_BLUE, task[0], COLOR_END, task[1])
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
                if line[:3] == '## ':
                    action = short_action_names[line[3:]]
                elif line[:2] == '* ':
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
        for action in short_action_names:
            text += put_list(action, short_action_names[action])
        return text

