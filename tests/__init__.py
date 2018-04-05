import os
import unittest


TESTS_HOME = os.path.abspath(os.path.dirname(__file__))
SAMPLES_HOME = os.path.join(TESTS_HOME, 'samples')


def load_sample(sample_name):
    sample_path = os.path.join(SAMPLES_HOME, sample_name)
    return open(sample_path, 'r')
