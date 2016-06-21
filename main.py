#!/usr/bin/env python3

# local imports
from util import *
from version import Version
from tasklist import TaskList
from changelog import Changelog

# system imports
import sys

todolist = TaskList('TODO', 'TODO.md')
changelog = Changelog('CHANGELOG', 'CHANGELOG.md')

if sys.argv[1] in ('todo', 't'):
    action = None
    if sys.argv[2] in ('list', 'ls', 'l'):
        actions = ['add', 'fix', 'rem', 'chg']
        if len(sys.argv[3:]) > 0:
            actions = sys.argv[3:]
        print(todolist.list(actions))
    elif sys.argv[2] in ('add', 'a'):
        action = 'add'
    elif sys.argv[2] in ('fix', 'f'):
        action = 'fix'
    elif sys.argv[2] in ('rem', 'remove', 'r'):
        action = 'rem'
    elif sys.argv[2] in ('chg', 'change', 'c'):
        action = 'chg'
    if action:
        todolist.add(action, sys.argv[3])
elif sys.argv[1] in ('do', 'd'):
    try:
        index = int(sys.argv[2])
        action, task = todolist.pop(index)
        changelog.add(action, task)
    except:
        raise ValueError
elif sys.argv[1] in ('version', 'ver', 'v'):
    if sys.argv[2]:
        version = Version(sys.argv[2])
        changelog.set_version(version)
    else:
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
