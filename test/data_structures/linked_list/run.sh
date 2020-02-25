#!/bin/bash
# Author: John Zlotek
# Date: 29 Jan 2020
#   Set up basic case switching for script
#
# Usage: read in config file and scrape for test
#        harness files and commands to run

source ./config

if [ $# -gt 1 ]; then
  OPTION='submit'
else
  OPTION=$1
fi

case $OPTION in
  submit)
    COMMAND=$SUBMIT_TEST
    ;;
  test)
    COMMAND=$USER_TEST
    ;;
  *)
    echo "Unknown option... $OPTION"
    exit 1
    ;;
esac

exec $COMMAND

