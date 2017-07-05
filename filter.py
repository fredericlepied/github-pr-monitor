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

import json
import sys

class Filter(object):
    def __init__(self, args):
        pass

    def process_file(self, filename):
        try:
            with open(filename) as f:
                data = json.loads(f.read(-1))
            if self.validate_data(data):
                print filename
        except Exception as e:
            sys.stderr.write('Error:%s: %s' % (filename, e))
            return

    def validate_data(self, data):
        return True

    def select(self, selector, data):
        keys = selector.split('.')
        if keys[-1] == '':
            keys = keys[:-1]
        for key in keys:
            data = data[key]
        return data
        

def main(cls):
    try:
        filter = cls(sys.argv[1:])
    except:
        sys.stderr.write('%s\n' % cls.__doc__)
        sys.exit(1)

    while True:
        filename = sys.stdin.readline().strip('\n')
        if filename == '':
            break
        filter.process_file(filename)
    sys.exit(0)

if __name__ == "__main__":
    main(Filter)

# filter.py ends here
