#!/usr/bin/env bash

set -e

source ~/.bin/dotfiles/.secrets.zconfig

function books {
  local library="$HOME/Documents/Calibre Library"
  local desination_dir="$HOME/synco/books"
  local sync_file="$HOME/synco/books/books-synced"
  local server_sync_file="$HOME/synco/books/server-books-synced"
  local temp_dir="$HOME/synco/books/books-to-sync"
  curl "http://192.168.0.46/synco/books/server-books-synced" > $server_sync_file
  rm $sync_file
  find "$library" -type f -name "*.mobi" | while read -r mobi_file; do
    filename=$(basename "$mobi_file")
    # ln -s "$mobi_file" "$destination_dir/$filename"
    # echo $filename
    echo $mobi_file >> $sync_file
  done

  mkdir -p $temp_dir
  diff $sync_file $server_sync_file | grep '^<' | sed 's/^< //' | while read -r mobi_file; do
    echo "$mobi_file"
    filename=$(basename "$mobi_file")
    cp "$mobi_file" "$temp_dir/$filename"
  done

  echo "about to sync $(ls $temp_dir | wc -l) books"
  scp -r $temp_dir shane@$NIGHTINGALE:~/synco/books/
  scp -r $sync_file shane@$NIGHTINGALE:~/synco/books/server-books-synced
  rm -r $temp_dir
}

books

