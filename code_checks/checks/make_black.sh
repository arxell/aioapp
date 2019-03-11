#!/bin/bash

for filepath in `git diff --name-only master | grep "^app/" | grep ".py$"`; do
    echo $filepath;
    black -S -l 80 $filepath;
done
