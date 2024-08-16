#!/usr/bin/env bash

set -e

yt-dlp -f "bestaudio/best" --extract-audio --audio-format mp3 "$1"
mv *.mp3 music
cd music
rename_convention
cd -
