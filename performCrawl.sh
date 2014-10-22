FILE_NAME=items-$(date | sed 's/[: ]/\-/g').json
touch $FILE_NAME
scrapy crawl LibraryThing -o $FILE_NAME
