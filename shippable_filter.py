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

import filter

class ShippableFilter(filter.Filter):
    'Usage: shippable_filter.py'
    def __init__(self, args):
        pass

    def validate_data(self, data):
        if 'statuses' not in data or 'sha' not in data:
            return False
        sha = data['sha']
        if sha not in data['statuses'] or len(data['statuses'][sha]) == 0:
            return False
        status = data['statuses'][sha][0]
        if 'state' not in status or 'context' not in status:
            return False
        if status['state'] == 'success' and status['context'] == 'Shippable':
            return True
        return False

if __name__ == "__main__":
    filter.main(ShippableFilter)

# shippable_filter.py ends here
