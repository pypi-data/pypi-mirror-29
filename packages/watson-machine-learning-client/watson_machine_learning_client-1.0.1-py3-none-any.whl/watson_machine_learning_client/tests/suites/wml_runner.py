import os
import unittest
import timeit
import sys
import xmlrunner
import datetime
from datetime import timedelta
from os.path import join as path_join
import plotly.graph_objs as go
import plotly


class WMLRunner:
    test_cases = []
    test_total = 0
    test_failed = 0
    test_succeeded = 0
    test_skipped = 0
    duration = timeit.default_timer()
    passrate_file = None
    passrate_filename = ""
    test_output_dir = ""
    chart_results = {}

    def __init__(self, test_cases, environment, spark_required=True, java_required=True,
                 passrate_filename="passrate", test_output_dir="test-reports", create_chart=False):

        self.test_cases = test_cases
        self.passrate_filename = passrate_filename
        self.test_output_dir = test_output_dir
        self.create_chart = create_chart

        if environment is not None:
            os.environ['ENV'] = environment

        if spark_required:
            if "SPARK_HOME" not in os.environ:
                print("Test suite interrupted, reason: SPARK_HOME is not set")
                quit()

            SPARK_HOME_PATH = os.environ['SPARK_HOME']
            PYSPARK_PATH = str(SPARK_HOME_PATH) + "/python/"
            sys.path.insert(1, path_join(PYSPARK_PATH))

        if java_required:
            if "JAVA_HOME" not in os.environ:
                print("Test suite interrupted, reason: JAVA_HOME is not set")
                quit()

    def single_run(self, test_cases):
        run_started_at = timeit.default_timer()
        runner = xmlrunner.XMLTestRunner(output="results/{}".format(self.test_output_dir))

        for test_case in test_cases:
            test_case_result = runner.run(test_case)

            self.test_total += test_case_result.testsRun
            self.test_failed += len(test_case_result.errors)
            self.test_skipped += len(test_case_result.skipped)

            if self.create_chart:
                current_data = datetime.datetime.now()
                current_data = current_data.replace(minute=0)
                current_data_string = current_data.strftime('%Y-%m-%d %H:%M')
                if current_data_string not in self.chart_results:
                    self.chart_results[current_data_string] = TestResult(total=test_case_result.testsRun, failures=len(test_case_result.errors))
                else:
                    self.chart_results[current_data_string].add(total=test_case_result.testsRun, failures=len(test_case_result.errors))

        current_duration = timeit.default_timer() - run_started_at
        self.duration += current_duration

    def save_all_runs(self):
        self.test_succeeded += self.test_total - self.test_failed
        self._save_results_to_passrate_file()

        if self.create_chart:
            self._save_result_chart()

    def run(self):
        run_started_at = timeit.default_timer()
        runner = xmlrunner.XMLTestRunner(output="results/{}".format(self.test_output_dir))

        for test_case in self.test_cases:
            test_case_result = runner.run(test_case)

            self.test_total += test_case_result.testsRun
            self.test_failed += len(test_case_result.errors)
            self.test_skipped += len(test_case_result.skipped)

        self.duration = timeit.default_timer() - run_started_at
        self.test_succeeded = self.test_total - self.test_failed

        self._save_results_to_passrate_file()

    def _format_duration_output(self):
        duration_delta = timedelta(seconds=self.duration)
        duration_output = ""

        if duration_delta.seconds // 3600 >= 0:
            duration_output += "{}hrs ".format(duration_delta.seconds // 3600)

        if duration_delta.seconds // 60 >= 0:
            duration_output += "{}mts ".format(duration_delta.seconds // 60 % 60)

        if duration_delta.seconds >= 0:
            duration_output += "{}sec".format(duration_delta.seconds % 60)

        return duration_output

    def _save_results_to_passrate_file(self):
        self._create_passrate_file()
        self._save_passrate_file()

    def _create_passrate_file(self):
        self.passrate_file = open("results/{}.prop".format(self.passrate_filename), "w")

    def _save_passrate_file(self):

        self.passrate_file.write("PASSRATE20={:05.2f}\n".format(self.test_succeeded / self.test_total * 100))

        self.passrate_file.write("Ignored_Tc={}\n".format(self.test_skipped))
        self.passrate_file.write("Succeeded={}\n".format(self.test_succeeded))
        self.passrate_file.write("Failed={}\n".format(self.test_failed))
        self.passrate_file.write("Total_Testcase={}\n".format(self.test_total))
        self.passrate_file.write("Duration={}\n".format(self._format_duration_output()))

        self.passrate_file.close()

    def _save_result_chart(self):

        results_list = sorted(list(self.chart_results.keys()))
        x_list = []
        y1_list = []
        y2_list = []
        y1_text = []
        y2_text = []
        for i in results_list:
            x_list.append(i)
            y1_list.append(self.chart_results[i].success)
            y2_list.append(self.chart_results[i].total)
            y1_text.append(self.chart_results[i].success)
            y2_text.append(self.chart_results[i].failures)

        trace0 = go.Scatter(
            x=x_list,
            y=y1_list,
            mode='lines',
            line=dict(width=0.5,
                      color='rgb(0, 153, 51)'),
            hoverinfo='x+text',
            text=y1_text,
            fill='tonexty',
            name="Success"
        )

        trace1 = go.Scatter(
            x=x_list,
            y=y2_list,
            mode='lines',
            line=dict(width=0.5,
                      color='rgb(230, 0, 0)'),
            hoverinfo='x+text',
            text=y2_text,
            fill='tonexty',
            name="Failures"
        )

        data = [trace0, trace1]
        layout = go.Layout(
            showlegend=True,
            xaxis=dict(
                type='category',
            ),
            yaxis=dict(
                type='linear'
            )
        )

        fig = go.Figure(data=data, layout=layout)
        plotly.offline.plot(fig, filename="results/result_chart.html")


class TestResult:

    total = 0
    success = 0
    failures = 0

    def __init__(self, total, failures):
        self.total += total
        self.success += (total - failures)
        self.failures += failures

    def add(self, total, failures):
        self.total += total
        self.success += (total - failures)
        self.failures += failures


def create_suite(test_module):
    loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    test_suite.addTest(loader.loadTestsFromModule(module=test_module))
    return test_suite
