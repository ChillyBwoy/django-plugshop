#!/usr/bin/env python

import os
import sys



os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, BASE_PATH)

def runtests(*args):
    from django.test.utils import get_runner
    from django.conf import settings
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2)
    failures = test_runner.run_tests(args)
    if failures:
        sys.exit(bool(failures))

if __name__ == '__main__':
    runtests(*sys.argv[1:])