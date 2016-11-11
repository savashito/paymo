#!/usr/bin/env bash

# example of the run script for running the fraud detection algorithm with a python file,
# but could be replaced with similar files from any major language

# I'll execute my programs, with the input directory paymo_input and output the files in the directory paymo_output
'/Users/rodrigosavage/Library/Enthought/Canopy_64bit/User/bin/Python' ./src/antifraud.py ./paymo_input/batch_payment.csv ./paymo_input/stream_payment.csv ./paymo_output/output1.txt ./paymo_output/output2.txt ./paymo_output/output3.txt

# echo $(date) $* >> $(pwd)/meow.txt
