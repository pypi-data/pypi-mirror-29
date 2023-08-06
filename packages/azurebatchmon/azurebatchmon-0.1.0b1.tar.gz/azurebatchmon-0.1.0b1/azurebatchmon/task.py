#! /usr/bin/env python

import sys, os

class Task:

    def __init__(self):
        
        self.env = {}
        self.inputs = {}
        self.input_recursive = {}
        self.outputs = {}
        self.output_recursive = {}

