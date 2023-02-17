#!/bin/sh

find *.jsonl -exec \
  sh \
    -c 'for f; do twarc2 network "$f" --format gml "${f%.jsonl}.gml"; done' \
    sh {} +
