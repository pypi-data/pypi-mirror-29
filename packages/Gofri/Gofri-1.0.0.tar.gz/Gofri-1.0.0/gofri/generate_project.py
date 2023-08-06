import os

import sys

import gofri.lib.project_generator.generator as G

if __name__ == '__main__':
    G.generate_project(os.getcwd(), sys.argv[1])