#!/bin/bash

LOGLEVEL=INFO python -m unittest discover -s recibundler -p '*_test.py' $@
