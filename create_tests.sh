#!/bin/bash

# use pyd2s_stat to create test cases for the item parser

save="$1"

pyd2s_stat "$save" -x -O tests/itemdata/new/

# remove duplicates
shopt -s nullglob
for f in tests/itemdata/new/*; do
  if [ -f tests/itemdata/"$(basename "$f")" ]; then
    rm "$f"
  fi
done

# write description files
shopt -s nullglob
for f in tests/itemdata/new/*.d2i; do
  echo "$f"
  pyd2s_stat "$f" -i | tail -n+2 > "${f%.d2i}.desc"
  cat "${f%.d2i}.desc"
done
