#!/bin/bash

for filepath in `git diff --name-only master | grep "^app/" | grep ".py$"`; do
    echo $filepath;
    isort -sp code_checks/checks $filepath;
done
