"""
Copyright 2012-2018 Ministerie van Sociale Zaken en Werkgelegenheid

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import datetime
import urllib.error
import unittest

from hqlib.metric_source import Jenkins
from hqlib.typing import DateTime


def to_jenkins_timestamp(date_time: DateTime, epoch: DateTime = datetime.datetime(1970, 1, 1)) -> int:
    """ Convert datetime instance to *milli*seconds since epoch. """
    delta = date_time - epoch
    return (delta.microseconds + (delta.seconds + delta.days * 24 * 3600) * 10**6) / 1000


class JenkinsUnderTest(Jenkins):  # pylint: disable=too-few-public-methods
    """ Override the url_open method to return a fixed HTML fragment. """
    contents = '{"jobs": []}'
    pipeline_contents = '{}'

    def url_read(self, url: str, *args, encoding: str = 'utf-8', **kwargs) -> str:  # pylint: disable=unused-argument
        """ Return the static content. """
        if 'raise' in url:
            raise urllib.error.URLError('some reason')
        elif '/job/' in url and 'tree=jobs[name,description,color,url,buildable]' in url:
            return self.pipeline_contents
        else:
            return self.contents


class JenkinsTest(unittest.TestCase):
    """ Unit tests for the Jenkins class. """

    def setUp(self):
        JenkinsUnderTest._api.cache_clear()
        self.__jenkins = JenkinsUnderTest('http://jenkins/', 'username', 'password')

    def test_url(self):
        """ Test the Jenkins url. """
        self.assertEqual('http://jenkins/', self.__jenkins.url())

    def test_no_failing_jobs(self):
        """ Test the number of failing jobs when there are no failing jobs. """
        self.assertEqual(0, self.__jenkins.number_of_failing_jobs())

    def test_no_failing_jobs_url(self):
        """ Test the number of failing jobs when there are no failing jobs. """
        self.assertEqual({}, self.__jenkins.failing_jobs_url())

    def test_one_failing_job(self):
        """ Test the failing jobs with one failing job. """
        date_time = datetime.datetime(2013, 4, 1, 12, 0, 0)
        self.__jenkins.contents = '{{"jobs": [{{"name": "job1", "color": "red", "description": "", ' \
                                  '"url": "http://jenkins/job/job1/", "buildable": True}}], "timestamp": "{}", ' \
                                  '"builds": [{{"result": "SUCCESS"}}]}}'.format(to_jenkins_timestamp(date_time))
        self.assertEqual(1, self.__jenkins.number_of_failing_jobs())

    def test_one_failing_job_url(self):
        """ Test the failing jobs with one failing job. """
        date_time = datetime.datetime(2013, 4, 1, 12, 0, 0)
        self.__jenkins.contents = '{{"jobs": [{{"name": "job1", "color": "red", "description": "", ' \
                                  '"url": "http://jenkins/job/job1/", "buildable": True}}], "timestamp": "{}", ' \
                                  '"builds": [{{"result": "SUCCESS"}}]}}'.format(to_jenkins_timestamp(date_time))
        expected_days_ago = (datetime.datetime.utcnow() - date_time).days
        self.assertEqual({'job1 ({0:d} dagen)'.format(expected_days_ago): 'http://jenkins/job/job1/'},
                         self.__jenkins.failing_jobs_url())

    def test_ignore_disabled_job(self):
        """ Test that disabled failing jobs are ignored. """
        self.__jenkins.contents = '{"jobs": [{"name": "job1", "color": "red", "description": "", ' \
                                  '"url": "http://jenkins/job/job1/", "buildable": False}], "builds": [{}]}'
        self.assertEqual({}, self.__jenkins.failing_jobs_url())

    def test_ignore_pipelines(self):
        """ Test that pipelines (jobs without buildable flag) are ignored. """
        self.__jenkins.contents = '{"jobs": [{"name": "job1", "color": "red", "description": "", ' \
                                  '"url": "http://jenkins/job/job1/"}], "builds": [{}]}'
        self.assertEqual({}, self.__jenkins.failing_jobs_url())

    def test_include_pipeline_job(self):
        """ Test that pipeline jobs are included. """
        timestamp = to_jenkins_timestamp(datetime.datetime.utcnow() - datetime.timedelta(days=100))
        self.__jenkins.pipeline_contents = '{"jobs": [{"name": "master", "color": "red", "description": "", ' \
                                           '"url": "http://jenkins/job/master/", "buildable": True}]}'
        self.__jenkins.contents = '{{"jobs": [{{"name": "job1", "color": "red", "description": "", ' \
                                  '"url": "http://jenkins/job/job1/"}}], "timestamp": "{}", ' \
                                  '"builds": [{{"result": "SUCCESS"}}]}}'.format(timestamp)
        self.assertEqual({'master (100 dagen)': 'http://jenkins/job/master/'}, self.__jenkins.failing_jobs_url())

    def test_failing_jobs_url(self):
        """ Test that the failing jobs url dictionary contains the url for the failing job. """
        timestamp = to_jenkins_timestamp(datetime.datetime.utcnow() - datetime.timedelta(days=100))
        self.__jenkins.contents = '{{"jobs": [{{"name": "job1", "color": "red", "description": "", ' \
                                  '"url": "http://jenkins/job/job1/", "buildable": True}}], "timestamp": "{}", ' \
                                  '"builds": [{{"result": "SUCCESS"}}]}}'.format(timestamp)
        self.assertEqual({'job1 (100 dagen)': 'http://jenkins/job/job1/'}, self.__jenkins.failing_jobs_url())

    def test_failing_jobs_url_no_description(self):
        """ Test that the failing jobs url works if there are jobs without description. """
        now = datetime.datetime.utcnow()
        jan_first = now.replace(month=1, day=1, hour=0, minute=0, second=0)
        if now.month == now.day == 1:  # pragma: no branch
            jan_first = jan_first.replace(year=jan_first.year - 1)  # pragma: no cover
        self.__jenkins.contents = '{{"jobs": [{{"name": "job1", "color": "red", "description": None, ' \
                                  '"url": "http://jenkins/job/job1/", "buildable":  True}}], "timestamp": "{}", ' \
                                  '"builds": [{{"result": "SUCCESS"}}]}}'.format(to_jenkins_timestamp(jan_first))
        expected_days_ago = (datetime.datetime.utcnow() - jan_first).days
        self.assertEqual({'job1 ({0:d} dagen)'.format(expected_days_ago): 'http://jenkins/job/job1/'},
                         self.__jenkins.failing_jobs_url())

    def test_no_unused_jobs(self):
        """ Test the number of unused jobs when there are no unused jobs. """
        self.assertEqual(0, self.__jenkins.number_of_unused_jobs())

    def test_no_unused_jobs_url(self):
        """ Test the number of unused jobs when there are no unused jobs. """
        self.assertEqual({}, self.__jenkins.unused_jobs_url())

    def test_one_unused_job(self):
        """ Test the unused jobs with one unused job. """
        date_time = datetime.datetime(2000, 4, 1, 12, 0, 0)
        self.__jenkins.contents = '{{"jobs": [{{"name": "job1", "color": "red", "description": "", ' \
                                  '"url": "http://jenkins/job/job1/", "buildable": True}}], ' \
                                  '"timestamp": "{}"}}'.format(to_jenkins_timestamp(date_time))
        self.assertEqual(1, self.__jenkins.number_of_unused_jobs())

    def test_one_unused_job_url(self):
        """ Test the unused jobs with one unused job. """
        date_time = datetime.datetime(2000, 4, 1, 12, 0, 0)
        self.__jenkins.contents = '{{"jobs": [{{"name": "job1", "color": "red", "description": "", ' \
                                  '"url": "http://jenkins/job/job1/", "buildable": True}}], ' \
                                  '"timestamp": "{}", "builds": [{{"result": "SUCCESS"}}]}}'.format(
                                      to_jenkins_timestamp(date_time))
        expected_days_ago = (datetime.datetime.utcnow() - date_time).days
        self.assertEqual({'job1 ({0:d} dagen)'.format(expected_days_ago): 'http://jenkins/job/job1/'},
                         self.__jenkins.unused_jobs_url())

    def test_unused_jobs_grace(self):
        """ Test the unused jobs with one unused job within grace time. """
        self.__jenkins.contents = '{{"jobs": [{{"name": "job1", "color": "red", "description": "[gracedays=400]", ' \
                                  '"url": "http://jenkins/job/job1/", "buildable": True}}], "timestamp": "{}", ' \
                                  '"builds": [{{"result": "SUCCESS"}}]}}'.format(
                                      to_jenkins_timestamp(datetime.datetime.utcnow() - datetime.timedelta(days=100)))
        self.assertEqual({}, self.__jenkins.unused_jobs_url())

    def test_unused_jobs_after_grace(self):
        """ Test the unused jobs with one unused job within grace time. """
        last_year = datetime.datetime.utcnow().year - 1
        self.__jenkins.contents = '{{"jobs": [{{"name": "job1", "color": "red", "description": "[gracedays=200]", ' \
                                  '"url": "http://jenkins/job/job1/", "buildable": True}}], "timestamp": "{}", ' \
                                  '"builds": [{{"result": "SUCCESS"}}]}}'.format(
                                      to_jenkins_timestamp(datetime.datetime(last_year, 1, 1, 12, 0, 0)))
        expected_days_ago = (datetime.datetime.utcnow() - datetime.datetime(last_year, 1, 1, 12, 0, 0)).days
        self.assertEqual({'job1 ({0:d} dagen)'.format(expected_days_ago): 'http://jenkins/job/job1/'},
                         self.__jenkins.unused_jobs_url())

    def test_nr_of_active_jobs(self):
        """ Test the number of active jobs. """
        self.assertEqual(0, self.__jenkins.number_of_active_jobs())

    def test_nr_of_active_jobs_on_error(self):
        """ Test that the number of active jobs is -1 when an URL error is thrown. """
        self.assertEqual(-1, JenkinsUnderTest('http://raise').number_of_active_jobs())

    def test_nr_of_failing_jobs_on_error(self):
        """ Test that the number of failing jobs is -1 when an URL error is thrown. """
        self.assertEqual(-1, JenkinsUnderTest('http://raise').number_of_failing_jobs())

    def test_nr_of_unused_jobs_on_error(self):
        """ Test that the number of unused jobs is -1 when an URL error is thrown. """
        self.assertEqual(-1, JenkinsUnderTest('http://raise').number_of_unused_jobs())
