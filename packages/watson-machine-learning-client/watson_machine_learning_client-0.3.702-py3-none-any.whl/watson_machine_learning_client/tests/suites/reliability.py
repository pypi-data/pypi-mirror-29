import unittest
import time
import sys
from wml_runner import *


if __name__ == '__main__':

    pattern = "test_scikit_learn*object.py"
    iteration = 1000

    if len(sys.argv) > 0:
        pattern = str(sys.argv[1])
        iteration = int(sys.argv[2])

    runner = WMLRunner(test_cases=None, environment="SVT", passrate_filename="reliability",
                       test_output_dir="reliability", spark_required=False, java_required=False, create_chart=True)

    for i in range(0, iteration):
        print("Run test: {}".format(i))
        test_case = unittest.TestLoader().discover(start_dir="../svt", pattern=pattern)
        runner.single_run(test_case)
        print("Test {} finished.".format(i))
        time.sleep(10)

    runner.save_all_runs()
