#!/bin/bash

for page_num in `seq 1 10`; do
    curl -G -H "Accept: application/vnd.github.v3+json" "https://api.github.com/search/repositories?q=stars:>1000&per_page=100&page=${page_num}" > stars_${page_num}.json
    sleep 3
done