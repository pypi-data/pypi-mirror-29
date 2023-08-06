#!/bin/bash

rm -f oboe.py oboe_wrap.cxx _oboe.so
swig -c++ -python oboe.i
