"""
This file is used to run pylint programmatically.
"""
import sys
from io import StringIO

from pylint.lint import Run
from pylint.reporters.text import TextReporter

is_success: bool = True

# python scripts/run_pylint.py [res of args]
opts = sys.argv[1:]
output = StringIO()
reporter = TextReporter(output)
result: Run = Run(opts, reporter=reporter, exit=False)

stats = result.linter.stats
score = stats.global_note

if score < 9.0:
    print("Pylint score {} is too low!")
    is_success = False
else:
    print("Pylint score is good!")

if not is_success:
    sys.exit(1)
