echo "book-scraper
============

Crawls LibraryThing to extract data from a LibraryThing user's catalog. If the LibraryThing user is me.

## Stats
### Most common places
$(jq '.[].places | select(.) | .[]' items.json | sort | uniq -c | sort -r | head -15 | while read line; do
    echo "- $line"
done )

### Centuries
$(jq '.[].date_first_published | select(.)' items.json | sed 's/"\(..\).*\"/\1/g' | sort | uniq -c | sort -r | head -5 | while read line; do
    echo "- `echo $line`00s"
done )

### Decades

$(jq '.[].date_first_published | select(.)' items.json | sed 's/"\(...\).\"/\1/g' | sort | uniq -c | sort -r | head -10 | while read line; do
    echo "- `echo $line`0s"
done )
" > README.md
