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

if [ $# != 3 ]; then
    echo "Usage: $0 <PR id> <project file> <sha 1>" 1>&2
    exit 1
fi

set -eux

PR=$1
FILE=$2
SHA1=$3

. "$FILE"

if [ -z "$PROJECT" ]; then
    echo "PROJECT unset in $FILE" 1>&2
    exit 1
fi

if [ ! -d $PROJECT-pr-data/$PROJECT ]; then
    dlrn --config-file ${PROJECT}-pr.ini --info-repo $PWD/${PROJECT}-pr-info --local --dev --package-name $(basename $PROJECT) --run /bin/true
fi

cd $PROJECT-pr-data/$PROJECT
git checkout master
git branch -D pr-$PR || :
git fetch origin pull/$PR/head:pr-$PR
git checkout pr-$PR

PROJECT_SHA=$(git rev-parse HEAD)

[ "$PROJECT_SHA" = "$SHA1" ]

cd ../${PROJECT}_distro
git checkout rpm-master || :
git checkout rpm-devel || :
git pull
git checkout pr-$PR || :

cd ../..

rm -rf $DLRN_CONF-data/repos/${SHA1:0:2}/${SHA1:2:2}/${SHA1}_dev

export COPR_ID

dlrn --config-file ${PROJECT}-pr.ini --info-repo $PWD/systemd-master-info --local --dev --package-name $(basename $PROJECT)

# extract-pr.sh ends here
