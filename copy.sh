#!/usr/bin/env bash
location=/.cache/ulauncher_cache/extensions/extensionlist/
killall ulauncher
mkdir -p $HOME${location}
rm -rf $HOME${location}*
cp -r * $HOME${location}
ulauncher -v