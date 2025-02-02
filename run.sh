#!/bin/bash

# Get the directory of the current script (where run.sh is located)
SCRIPT_DIR=$(dirname "$(realpath "$0")")

# Ensure the 'music' directory exists
mkdir -p "$SCRIPT_DIR/music"

# Run yt-dlp and save files in the 'music' directory
yt-dlp -f bestaudio[ext=m4a]/bestaudio --audio-quality 0 --extract-audio --audio-format mp3 -o "$SCRIPT_DIR/music/%(title)s.%(ext)s" -a "$SCRIPT_DIR/url_list.txt"
