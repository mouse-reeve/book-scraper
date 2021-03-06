#!/bin/bash

echo "book-scraper
============

Crawls LibraryThing to extract data from a LibraryThing user's catalog. If the LibraryThing user is me.

## Stats
### Most common places
$(jq '.[].places | select(.) | .[]' items.json | sort | uniq -c | sort -r | head -15 | while read line; do
    echo "- $line"
done )

### Century of first publication
$(jq '.[].date_first_published | select(.)' items.json | grep "\d\+" | sed 's/"\(..\).*\"/\1/g' | sort | uniq -c | sort -r | head -5 | while read line; do
    echo "- `echo $line`00s"
done )

### Decade of fist publication

$(jq '.[].date_first_published | select(.)' items.json | sed 's/"\(...\).\"/\1/g' | sort | uniq -c | sort -r | head -10 | while read line; do
    echo "- `echo $line`0s"
done )
" > README.md
