#!/bin/bash

# See https://github.com/paul-hammant/browser-download-deleter

/usr/local/bin/fswatch -xnr ~/Downloads/ | xargs -n1 /usr/local/bin/browser-download-deleter-via-dialog.py