#!/bin/bash

for mpq in d2data d2exp Patch_D2; do
  if [ ! -f "$mpq.mpq" ]; then
    echo "Error: missing $mpq.mpq" >&2
    exit 1 
  fi
done

rm -rf d2data/
rm -rf d2exp/
rm -rf Patch_D2/

for mpq in d2data d2exp Patch_D2; do
  MPQExtractor -a listfile.txt \
               -e '*' \
               -o "$mpq/" \
               -f \
               -c \
               "$mpq.mpq"
done

# apply patch to d2exp
cp -r Patch_D2/data d2exp/ 
