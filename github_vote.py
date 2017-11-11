#!/usr/bin/env python
#
# Copyright (C) 2017 Red Hat, Inc. 
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

from github import (Github, GithubObject)

if len(sys.argv) not in (6, 7):
    print(
        'Usage: %s <repository> <sha> (success|pending|failure|error) <context> <detail>'
        '[<url>]'
        % sys.argv[0])
    sys.exit(1)

reponame = sys.argv[1]
sha = sys.argv[2]
state = sys.argv[3]
context = sys.argv[4]
detail = sys.argv[5]

if len(sys.argv) == 7:
    url = sys.argv[6]
else:
    url = GithubObject.NotSet

if state not in ('success', 'failure', 'pending', 'error'):
    print('Unknown state %s' % state)
    sys.exit(1)

gh_handler = Github(open('github.key').read(-1).strip())

repo = gh_handler.get_repo(reponame)

commit = repo.get_commit(sha)
commit.create_status(state, url, detail, context)

# github_vote.py ends here
