#!/bin/bash

target_dir="$1"
find "$target_dir" -type f -print0 | while read -d $'\0' file; do
    echo "Content of file $file:"
    cat "$file"
    echo ""
done
