#!/usr/bin/env python
#
# Copyright (C) 2017 Red Hat, Inc. 
#
# Author: Frederic Lepied <frederic.lepied@redhat.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

'''
'''

import itertools
import json
import os
import sys
import time

from github import Github

def check_rate_limit(github, nb_req=1):
    print(github.rate_limiting, github.rate_limiting_resettime)
    if github.rate_limiting[0] == 0:
        secs = github.rate_limiting_resettime - int(time.time())
        print('Sleeping for %d s' % secs)
        time.sleep(secs)
    elif github.rate_limiting[1] > github.rate_limiting[0]:
        secs = (nb_req * (github.rate_limiting_resettime - int(time.time())) //
                (github.rate_limiting[0] + 1)) + 1
        print('Rate limiting for %d s' % secs)
        time.sleep(secs)

if len(sys.argv) not in (4, 5, 6):
    print(
        'Usage: %s <repository name> <target directory> <key> '
        '[<user> <password>|<token>]'
        % sys.argv[0])
    sys.exit(1)

reponame = sys.argv[1]
target_dir = sys.argv[2]
key = sys.argv[3]

if len(sys.argv) == 5:
    gh_handler = Github(sys.argv[4])
elif len(sys.argv) == 6:
    gh_handler = Github(sys.argv[4], sys.argv[5])
else:
    gh_handler = Github()

#check_rate_limit(gh_handler)
repo = gh_handler.get_repo(reponame)
check_rate_limit(gh_handler)

for pr in repo.get_pulls():
    print('processing PR %d' % pr.number)
    print(pr)
    filename = os.path.join(target_dir, str(pr.number))
    if os.path.exists(filename):
        try:
            with open(filename) as f:
                old = json.loads(f.read(-1))
                if old['updated_at'] == time.mktime(pr.updated_at.timetuple()):
                    print('Already up-to-date')
                    old['key'] = key
                    # update all the data that don't need other calls
                    old['number'] = pr.number
                    old['title'] = pr.title
                    old['state'] = pr.state
                    old['sha'] = pr.head.sha
                    old['mergeable'] = pr.mergeable
                    old['created_at'] = time.mktime(pr.created_at.timetuple())
                    with open(filename, 'w') as tosave:
                        tosave.write(json.dumps(old))
                    continue
        except Exception as e:
            print('Error reading %s: %s' % (filename, e))
    d = {}
    d['key'] = key
    d['number'] = pr.number
    d['title'] = pr.title
    d['state'] = pr.state
    d['sha'] = pr.head.sha
    d['mergeable'] = pr.mergeable
    d['updated_at'] = time.mktime(pr.updated_at.timetuple())
    d['created_at'] = time.mktime(pr.created_at.timetuple())
    d['files'] = [f.filename for f in pr.get_files()]
    statuses = {}
    for commit in pr.get_commits():
        statuses[commit.sha] = [{'state': s.state, 'id': s.id, 'context': s.context,
                                 'updated_at': time.mktime(s.updated_at.timetuple())}
                                for s in commit.get_statuses()]
    issue = repo.get_issue(pr.number)
    if issue:
        d['labels'] = [l.name for l in issue.labels]
    else:
        d['labels'] = []
    d['statuses'] = statuses
    with open(filename, 'w') as f:
        f.write(json.dumps(d))
    check_rate_limit(gh_handler, 3)

# get_pull_requests.py ends here
