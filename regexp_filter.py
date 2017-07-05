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

from operator import itemgetter
import re
import sys

import filter


class RegexpFilter(filter.Filter):
    'Usage: regexp_filter.py <key> <regexp>'
    def __init__(self, args):
        self.selector = args[0]
        self.regexp = re.compile(args[1])

    def validate_data(self, data):
        data = self.select(self.selector, data)
        #print(data)
        if type(data) is list or type(data) is tuple:
            # at least one item matching regexp
            for filename in data:
                if self.regexp.search(filename):
                    sys.stderr.write('%s\n' % filename)
                    return True
        else:
            if not isinstance(data, basestring):
                data = str(data)
            return self.regexp.search(data)
        return False

if __name__ == "__main__":
    filter.main(RegexpFilter)

# regexp_filter.py ends here
