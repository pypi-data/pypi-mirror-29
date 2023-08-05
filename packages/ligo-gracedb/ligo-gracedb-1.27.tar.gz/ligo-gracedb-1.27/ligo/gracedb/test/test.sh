#!/bin/bash

# -*- coding: utf-8 -*-
# Copyright (C) Brian Moe, Branson Stephens (2015)
#
# This file is part of gracedb
#
# gracedb is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# It is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gracedb.  If not, see <http://www.gnu.org/licenses/>.


# Tests for the gracedb command-line client
: ${GRACEDB:="gracedb"}
: ${TEST_DATA_DIR:=$(dirname $0)/data}
: ${TEST_SERVICE:="https://gracedb-test.ligo.org/api/"}

# Set up GRACEDB_SERVICE_URL for calls to the
# command-line client
export GRACEDB_SERVICE_URL=${TEST_SERVICE}

# Variables for tracking number of successes and failures
N=0
NSUCC=0
NFAIL=0
NERR=0

# Utility function for recording test results
function recordTest() {
    TESTNAME=$1
    RETCODE=$2
    OUT="$3"
    case $RETCODE in
        0)  NSUCC=$[$NSUCC+1]
            MESSAGE="Succeeded"
            ;;
        1)  NFAIL=$[$NFAIL+1]
            MESSAGE="Failed $OUT"
            ;;
        *)  NERR=$[$NERR+1]
            MESSAGE="Error $OUT"
            ;;
    esac
    N=$[$N+1]
    echo $TESTNAME $MESSAGE
}

# Utility function for showing results at end of testing
function showStats() {
    echo "Success: " $NSUCC
    echo "Fail:    " $NFAIL
    echo "Error:   " $NERR
    echo "Total:   " $N
}

# Print server being used for tests
echo "Using server ${GRACEDB_SERVICE_URL} for command-line client tests"

# Test ping
OUT="$(${GRACEDB} ping 2>&1)"
recordTest "ping" "$?" "$OUT"

# Create a gstlal low-mass event which we will use later
OUT="$(${GRACEDB} Test gstlal LowMass $TEST_DATA_DIR/cbc-lm.xml --labels=EM_READY,INJ --offline 2>&1)"
RETCODE=$?
recordTest "create gstlal" "$RETCODE" "$OUT"
if [ $RETCODE -eq 0 ]
then
    GRACEID=$OUT
else
    GRACEID="NOID"
fi

# Create an MBTA event
OUTFILE=$(mktemp /tmp/tmp.XXXXXXXXX)
${GRACEDB} Test MBTAOnline $TEST_DATA_DIR/cbc-mbta.xml >$OUTFILE 2>&1
recordTest "create MBTA" "$?" "$(cat $OUTFILE)"
rm $OUTFILE

# Create a CWB event
OUTFILE=$(mktemp /tmp/tmp.XXXXXXXXX)
${GRACEDB} Test CWB $TEST_DATA_DIR/burst-cwb.txt >$OUTFILE 2>&1
recordTest "create CWB"  "$?" "$(cat $OUTFILE)"
rm $OUTFILE

# Try a simple search
OUTFILE=$(mktemp /tmp/tmp.XXXXXXXXX)
${GRACEDB} search $GRACEID >$OUTFILE 2>&1
recordTest "search $GRACEID" "$?" "$(cat $OUTFILE)"
rm $OUTFILE

# Try a simple search with ligolw output.
OUTFILE=$(mktemp /tmp/tmp.XXXXXXXXX)
${GRACEDB} search $GRACEID --ligolw >$OUTFILE 2>&1
recordTest "search $GRACEID --ligolw" "$?" "$(cat $OUTFILE)"
rm $OUTFILE

# Make sure FAR of created LM event is correct.
OUTFILE=$(mktemp /tmp/tmp.XXXXXXXXX)
${GRACEDB} search "--columns=gpstime" $GRACEID > $OUTFILE 2>&1
RETCODE=$?
if [ $RETCODE == 0 ]
then
    if [ "$(grep -v '#' <$OUTFILE)" == 971609248.152 ]
    then
        RETCODE=0
    else
        RETCODE=1
    fi
fi
recordTest "verify GPS time $GRACEID" "$RETCODE" "$(cat $OUTFILE)"
rm $OUTFILE

# Replace LM event with new data
OUTFILE=$(mktemp /tmp/tmp.XXXXXXXXX)
${GRACEDB} replace $GRACEID $TEST_DATA_DIR/cbc-lm2.xml >$OUTFILE 2>&1
RETCODE=$?
recordTest "replace $GRACEID" "$RETCODE" "$(cat $OUTFILE)"
rm $OUTFILE


# Make sure FAR of replaced LM event is correct.
OUTFILE=$(mktemp /tmp/tmp.XXXXXXXXX)
${GRACEDB} search "--columns=gpstime" $GRACEID > $OUTFILE 2>&1
RETCODE=$?
if [ $RETCODE == 0 ]
then
    if [ "$(grep -v '#' <$OUTFILE)" == 971609249.152 ]
    then
        RETCODE=0
    else
        RETCODE=1
    fi
fi
recordTest "verify new GPS time $GRACEID" "$RETCODE" "$(cat $OUTFILE)"
rm $OUTFILE

# Upload a file
OUTFILE=$(mktemp /tmp/tmp.XXXXXXXXX)
${GRACEDB} --tag-name=tag_test upload $GRACEID "$TEST_DATA_DIR/upload.data.gz" > $OUTFILE 2>&1
recordTest "upload file $GRACEID" "$?" "$(cat $OUTFILE)"
rm $OUTFILE

# Download that uploaded file
DOWNLOAD=$(mktemp /tmp/tmp.XXXXXXXXX)
${GRACEDB} download $GRACEID "upload.data.gz" - > $DOWNLOAD 2>&1
recordTest "download file" "$?" "$(cat $DOWNLOAD)"

# Verify that the uploaded file and downloaded file were the same
cmp --silent "$DOWNLOAD" "$TEST_DATA_DIR/upload.data.gz"
recordTest "verify uploaded file" "$?" "$(cat $DOWNLOAD)"
rm $DOWNLOAD

# Log
OUTFILE=$(mktemp /tmp/tmp.XXXXXXXXX)
${GRACEDB} log $GRACEID "test the" "logging" > $OUTFILE 2>&1
recordTest "log message" "$?" "$(cat $OUTFILE)"
rm $OUTFILE

# Verify initial labeling of EM_READY and INJ
OUTFILE=$(mktemp /tmp/tmp.XXXXXXXXX)
${GRACEDB} search $GRACEID | grep "EM_READY" | grep "INJ" > $OUTFILE 2>&1
recordTest "verify initial labels $GRACEID" "$?" "$(cat $OUTFILE)"
rm $OUTFILE

# Add DQV label
OUTFILE=$(mktemp /tmp/tmp.XXXXXXXXX)
${GRACEDB} label $GRACEID DQV > $OUTFILE 2>&1
recordTest "label $GRACEID" "$?" "$(cat $OUTFILE)"
rm $OUTFILE

# Verify all labels, including recently added DQV
OUTFILE=$(mktemp /tmp/tmp.XXXXXXXXX)
${GRACEDB} search $GRACEID | grep "DQV" | grep "EM_READY" | grep "INJ" > $OUTFILE 2>&1
recordTest "verify added label" "$?" "$(cat $OUTFILE)"
rm $OUTFILE

# Tag
OUTFILE=$(mktemp /tmp/tmp.XXXXXXXXX)
${GRACEDB} tag $GRACEID 1 tag_test > $OUTFILE 2>&1
recordTest "tag event" "$?" "$(cat $OUTFILE)"
rm $OUTFILE

# Delete tag
OUTFILE=$(mktemp /tmp/tmp.XXXXXXXXX)
${GRACEDB} delete_tag $GRACEID 1 tag_test > $OUTFILE 2>&1
recordTest "delete tag" "$?" "$(cat $OUTFILE)"
rm $OUTFILE

# Check offline variable
OUTFILE=$(mktemp /tmp/tmp.XXXXXXXXX)
${GRACEDB} search --columns=offline $GRACEID | grep True > $OUTFILE 2>&1
recordTest "check offline" "$?" "$(cat $OUTFILE)"
rm $OUTFILE

showStats

