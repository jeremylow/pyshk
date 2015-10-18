#!/bin/bash

watchmedo shell-command \
              --patterns="*.rst" \
              --ignore-pattern='build/*' \
              --recursive \
              --command='make html'