import uuid
import unittest
import os
import hashlib
import six
import tempfile
from timeout_decorator import timeout

from .completion_service import CompletionService

from studio.util import has_aws_credentials, filehash
from studio.util import download_file, rand_string

_file_url = 'https://s3-us-west-2.amazonaws.com/ml-enn/' + \
            'deepbilevel_datafiles/' + \
            'mightyai_combined_vocab/mightyai_miscfiles.tar.gz'

_file_s3 = 's3://s3-us-west-2.amazonaws.com/studioml-test/t.txt'

LOCAL_TEST_TIMEOUT = 600
CLOUD_TEST_TIMEOUT = 800


class CompletionServiceTest(unittest.TestCase):

    def _run_test(self,
                  args=None,
                  files={},
                  jobfile=None,
                  expected_results=None,
                  **csargs):

        if not(any(csargs)):
            return

        mypath = os.path.dirname(os.path.realpath(__file__))
        jobfile = os.path.join(
            mypath, jobfile or 'completion_service_testfunc.py')

        args = args or [0, 1]

        expected_results = expected_results or args
        submission_indices = {}
        n_experiments = len(args)
        experimentId = str(uuid.uuid4())

        with CompletionService(experimentId, **csargs) as cs:
            for i in range(0, n_experiments):
                key = cs.submitTaskWithFiles(jobfile, args[i], files)
                submission_indices[key] = i

            for i in range(0, n_experiments):
                result = cs.getResults(blocking=True)
                self.assertEquals(
                    result[1],
                    expected_results[submission_indices[result[0]]]
                )

    def _run_test_files(self,
                        files,
                        n_experiments=2,
                        **csargs):

        expected_results = [(i, self._get_file_hashes(files))
                            for i in range(n_experiments)]
        args = range(n_experiments)
        self._run_test(
            args=args,
            files=files,
            jobfile='completion_service_testfunc_files.py',
            expected_results=expected_results,
            **csargs
        )

    def _get_file_hashes(self, files):
        retval = {}
        for k, v in six.iteritems(files):
            if '://' in v:
                tmpfilename = os.path.join(
                    tempfile.gettempdir(), rand_string(10))
                download_file(v, tmpfilename)
                retval[k] = filehash(tmpfilename, hashobj=hashlib.md5())
                os.remove(tmpfilename)
            else:
                retval[k] = filehash(v, hashobj=hashlib.md5())

        return retval

    @unittest.skipIf(not has_aws_credentials(),
                     'AWS credentials needed for this test')
    @timeout(CLOUD_TEST_TIMEOUT, use_signals=False)
    def test_two_experiments_ec2(self):
        mypath = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(
            mypath,
            '..',
            'tests',
            'test_config_http_client.yaml')

        self._run_test(
            config=config_path,
            cloud_timeout=100,
            cloud='ec2')

    @unittest.skipIf(not has_aws_credentials(),
                     'AWS credentials needed for this test')
    @timeout(CLOUD_TEST_TIMEOUT, use_signals=False)
    def test_two_experiments_ec2spot(self):
        mypath = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(
            mypath,
            '..',
            'tests',
            'test_config_http_client.yaml')

        files_in_workspace = os.listdir(mypath)
        files = {f: os.path.join(mypath, f) for f in files_in_workspace if
                 os.path.isfile(os.path.join(mypath, f))}

        files['url'] = _file_url
        files['s3'] = _file_s3

        self._run_test_files(
            files=files,
            n_experiments=2,
            config=config_path,
            cloud_timeout=100,
            cloud='ec2spot',
        )

    @unittest.skip('TODO peterz fix in parallel mode')
    @timeout(LOCAL_TEST_TIMEOUT, use_signals=False)
    def test_two_experiments_apiserver(self):
        mypath = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(
            mypath,
            '..',
            'tests',
            'test_config_http_client.yaml')

        files_in_workspace = os.listdir(mypath)
        files = {f: os.path.join(mypath, f) for f in files_in_workspace if
                 os.path.isfile(os.path.join(mypath, f))}

        files['url'] = _file_url

        if has_aws_credentials():
            files['s3'] = _file_s3

        self._run_test_files(
            n_experiments=2,
            files=files,
            config=config_path)

    @unittest.skipIf(
        'GOOGLE_APPLICATION_CREDENTIALS' not in os.environ.keys(),
        'Need GOOGLE_APPLICATION_CREDENTIALS env variable to' +
        'use google cloud')
    @timeout(CLOUD_TEST_TIMEOUT, use_signals=False)
    def test_two_experiments_gcspot(self):
        mypath = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(
            mypath,
            '..',
            'tests',
            'test_config_http_client.yaml')

        files_in_workspace = os.listdir(mypath)
        files = {f: os.path.join(mypath, f) for f in files_in_workspace if
                 os.path.isfile(os.path.join(mypath, f))}

        files['url'] = _file_url

        self._run_test_files(
            files=files,
            n_experiments=2,
            config=config_path,
            cloud='gcspot')

    @unittest.skipIf(
        'GOOGLE_APPLICATION_CREDENTIALS_DC' not in os.environ.keys(),
        'Need GOOGLE_APPLICATION_CREDENTIALS_DC env variable to' +
        'use google cloud')
    @timeout(CLOUD_TEST_TIMEOUT, use_signals=False)
    def test_two_experiments_datacenter(self):
        oldcred = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = \
            os.environ['GOOGLE_APPLICATION_CREDENTIALS_DC']

        mypath = os.path.dirname(os.path.realpath(__file__))
        queue_name = 'test_queue_' + str(uuid.uuid4())
        config_path = os.path.join(
            mypath,
            '..',
            'tests',
            'test_config_datacenter.yaml')

        files_in_workspace = os.listdir(mypath)
        files = {f: os.path.join(mypath, f) for f in files_in_workspace if
                 os.path.isfile(os.path.join(mypath, f))}

        # files['url'] = _file_url
        files['s3'] = _file_s3

        self._run_test_files(
            files=files,
            config=config_path,
            queue=queue_name,
            shutdown_del_queue=True
        )
        if oldcred:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = oldcred

    @unittest.skipIf(
        'GOOGLE_APPLICATION_CREDENTIALS' not in os.environ.keys(),
        'Need GOOGLE_APPLICATION_CREDENTIALS env variable to' +
        'use google cloud')
    @timeout(CLOUD_TEST_TIMEOUT, use_signals=False)
    def test_two_experiments_gcloud(self):
        mypath = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(
            mypath,
            '..',
            'tests',
            'test_config_http_client.yaml')

        files_in_workspace = os.listdir(mypath)
        files = {f: os.path.join(mypath, f) for f in files_in_workspace if
                 os.path.isfile(os.path.join(mypath, f))}

        files['url'] = _file_url

        self._run_test_files(
            files=files,
            n_experiments=2,
            config=config_path,
            cloud='gcloud')


if __name__ == '__main__':
    unittest.main()
