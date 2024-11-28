#!/usr/bin/env bash

set -e

source ~/.bin/dotfiles/.secrets.zconfig

function books {
  local library="$HOME/Documents/Calibre Library"
  local desination_dir="$HOME/synco/books"
  local sync_file="$HOME/synco/books/books-synced"
  local server_sync_file="$HOME/synco/books/server-books-synced"
  local temp_dir="$HOME/synco/books/books-to-sync"
  curl "http://$NIGHTINGALE/synco/books/server-books-synced" > $server_sync_file
  rm $sync_file
  # Pull the mobi files from Calibre's library
  find "$library" -type f -name "*.mobi" | while read -r mobi_file; do
    filename=$(basename "$mobi_file")
    echo $mobi_file >> $sync_file
  done

  mkdir -p $temp_dir
  # Find the difference between what the server has or has had in the past and
  # what we have, then send only those files
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

function generic_sync {
  local type=$1 # e.g audiobooks
  # -a (archive): This option preserves the permissions, timestamps, symbolic links, and other file attributes.
  # -v (verbose): This option shows the progress of the operation.
  # -u: ignore files that haven't changed
  # --ignore-existing: This option ensures that existing files on the server will not be overwritten. Only files that don't exist on the server will be copied.
  rsync -av --ignore-existing "$HOME/synco/$type/" shane@$NIGHTINGALE:~/synco/$type/
}

function media_sync {
  # rsync -av --ignore-existing "$HOME/synco/media/" shane@$NIGHTINGALE:~/typhon/media/
  rsync -av --ignore-existing "$HOME/synco/media/films/" shane@$NIGHTINGALE:/mnt/typhon/media/films
  rsync -av --ignore-existing "$HOME/synco/media/tv/" shane@$NIGHTINGALE:/mnt/typhon/media/tv
  rsync -av --ignore-existing "$HOME/synco/media/music" shane@$NIGHTINGALE:/mnt/typhon/music
}

books
generic_sync "audiobooks"
generic_sync "music"
media_sync
