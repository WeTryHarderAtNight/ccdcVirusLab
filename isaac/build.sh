#!/bin/bash
pyinstaller listener.py -F  --clean --name not_ntpd
rm -rf build/
cp dist/* .
rm -rf dist/
rm not_ntpd.spec
