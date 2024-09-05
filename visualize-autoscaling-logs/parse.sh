#!/usr/bin/bash

mkdir -p "$RES_DIR/clean"
RESULT_PATH=$RES_DIR python clean.py
RESULT_PATH=$RES_DIR python stats.py
