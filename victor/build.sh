#!/bin/bash
mkdir compiled
cp cantstopthis ./compiled
pyinstaller \[systemdeamond\] -F -n \[systemdeamond\]
rm -rf build/
cp dist/* ./compiled
rm -rf dist/
rm \[systemdeamond\].spec 
