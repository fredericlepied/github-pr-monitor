#!/bin/bash
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

if [ $# != 1 -o ! -r "$1" ]; then
    echo "Usage: $0 <project file>" 1>&2
    exit 1
fi

set -x

filter() {
    cat
}

FILE="$1"
. "$FILE"

if [ -z "$PROJECT" ]; then
    echo "PROJECT unset in $FILE" 1>&2
    exit 1
fi

if [ -z "$GITHUB_ACCOUNT" ]; then
    GITHUB_ACCOUNT=$PROJECT
fi

mkdir -p $PROJECT/prs $PROJECT/todo $PROJECT/new $PROJECT/done $PROJECT/merged

while :; do
    KEY=$(echo $RANDOM|md5sum|cut -f1 -d' ')
    ./get_pull_requests.py $GITHUB_ACCOUNT/$PROJECT $PROJECT/prs:$PROJECT/done $KEY
    cd $PROJECT/prs
    # move prs
    ls | ../../regexp_filter.py key $KEY
    mv $(ls | ../../regexp_filter.py key $KEY) ../new
    # move the remaining ones that have been merged or deleted
    mv -f * ../merged
    # get back the existing ones
    mv -f ../new/* .
    # filter the prs with a tests label
    cp $(ls | filter) ../todo
    # remove already processed prs
    cd ../todo
    for pr in $(ls); do
        if [ -r ../done/$pr ] && [ "$(jq -r .sha $pr)" = "$(jq -r .sha ../done/$pr)" ]; then
            rm -f $pr
        fi
    done
    # back to top dir
    cd ../..
    exit
done

# download-prs-metadata.sh ends here
