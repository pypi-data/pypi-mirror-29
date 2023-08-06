#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


################################################################################
# Aftermath.
################################################################################


# relink brewed pythons
brew link python@2 --force --overwrite > /dev/null 2>&1
brew link python --overwrite > /dev/null 2>&1
brew link pypy --overwrite > /dev/null 2>&1
brew link pypy3 --overwrite > /dev/null 2>&1


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
