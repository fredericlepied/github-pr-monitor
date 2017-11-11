#!/bin/bash

if [ $# != 1 -o ! -r "$1" ]; then
    echo "Usage: $0 <project file>" 1>&2
    exit 1
fi

set -x

dir=$(cd $(dirname $0); pwd)

FILE="$1"
. "$FILE"

if [ -z "$PROJECT" ]; then
    echo "PROJECT unset in $FILE" 1>&2
    exit 1
fi

if [ -z "$SERVER_URL" ]; then
    echo "SERVER_URL unset in $FILE" 1>&2
    exit 1
fi

if [ -z "$GITHUB_ACCOUNT" ]; then
    GITHUB_ACCOUNT=$PROJECT
fi

mkdir -p $PROJECT/success $PROJECT/failure

for pr in $(ls $PROJECT/todo); do
    ts=$(jq .updated_at $PROJECT/todo/$pr)
    sha=$(jq -r .sha $PROJECT/todo/$pr)
    echo "$ts $pr $sha"
done | sort -rn | while read times pullreq sha1; do
    (
	echo "========================================"
	date
	$dir/github_vote.py $GITHUB_ACCOUNT/$PROJECT $sha1 pending "$CI_CONTEXT" "$CI_DETAIL pending"
	mv $PROJECT/todo/$pullreq $PROJECT/done/$pullreq
	cd $HOME/DLRN
	if $dir/extract-pr.sh $pullreq $FILE $sha1; then
	    ln -f $dir/$PROJECT/done/$pullreq $dir/$PROJECT/success/$pullreq
	    $dir/github_vote.py $GITHUB_ACCOUNT/$PROJECT $sha1 success "$CI_CONTEXT" "$CI_DETAIL succeeded" $SERVER_URL/$PROJECT-pr/${sha1:0:2}/${sha1:2:2}/${sha1}_dev/
	else
	    ln -f $dir/$PROJECT/done/$pullreq $dir/$PROJECT/failure/$pullreq
	    $dir/github_vote.py $GITHUB_ACCOUNT/$PROJECT $sha1 failure "$CI_CONTEXT" "$CI_DETAIL failed" $SERVER_URL/$PROJECT-pr/${sha1:0:2}/${sha1:2:2}/${sha1}_dev/build.log.gz
	fi
    )
    [ -f stop ] && exit
done
