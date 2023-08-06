# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import signal
import subprocess
from distutils import spawn

import testtools


class TestCli(testtools.TestCase):

    @testtools.skipUnless(spawn.find_executable("memcached"),
                          "memcached not found")
    def test_cli(self):
        self.assertEqual(0, os.system(
            "pifpaf run memcached --port 11216 echo >/dev/null 2>&1"))

    @staticmethod
    def _read_stdout_and_kill(stdout):
        env = {}
        for line in stdout.split(b'\n'):
            k, _, v = line.partition(b"=")
            env[k] = v
        os.kill(int(env[b"export PIFPAF_PID"].strip(b"\" \n;")),
                signal.SIGTERM)
        return env

    @testtools.skipUnless(spawn.find_executable("memcached"),
                          "memcached not found")
    def test_eval(self):
        c = subprocess.Popen(["pifpaf", "run", "memcached", "--port", "11219"],
                             stdout=subprocess.PIPE)
        (stdout, stderr) = c.communicate()
        self.assertEqual(0, c.wait())
        env = self._read_stdout_and_kill(stdout)

        self.assertEqual(b"\"memcached://localhost:11219\";",
                         env[b"export PIFPAF_URL"])
        self.assertEqual(b"\"memcached://localhost:11219\";",
                         env[b"export PIFPAF_MEMCACHED_URL"])

    @testtools.skipUnless(spawn.find_executable("memcached"),
                          "memcached not found")
    def test_exit_code(self):
        c = subprocess.Popen(["pifpaf", "run", "memcached", "--port", "11234",
                              "--", "bash", "-c", "exit 31"],
                             stdout=subprocess.PIPE)
        (stdout, stderr) = c.communicate()
        self.assertEqual(31, c.wait())

    @testtools.skipUnless(spawn.find_executable("memcached"),
                          "memcached not found")
    def test_env_prefix(self):
        c = subprocess.Popen(["pifpaf", "run",
                              "--env-prefix", "FOOBAR",
                              "memcached", "--port", "11215"],
                             bufsize=0,
                             stdout=subprocess.PIPE)
        (stdout, stderr) = c.communicate()
        self.assertEqual(0, c.wait())
        env = self._read_stdout_and_kill(stdout)

        self.assertEqual(b"\"memcached://localhost:11215\";",
                         env[b"export FOOBAR_URL"])
        self.assertEqual(b"\"memcached://localhost:11215\";",
                         env[b"export FOOBAR_MEMCACHED_URL"])
        self.assertEqual(env[b"export PIFPAF_PID"],
                         env[b"export FOOBAR_PID"])

    @testtools.skipUnless(spawn.find_executable("memcached"),
                          "memcached not found")
    def test_env_prefix_old_format(self):
        # Old format
        c = subprocess.Popen(["pifpaf",
                              "--env-prefix", "FOOBAR",
                              "run", "memcached", "--port", "11215"],
                             bufsize=0,
                             stdout=subprocess.PIPE)
        (stdout, stderr) = c.communicate()
        self.assertEqual(0, c.wait())
        env = self._read_stdout_and_kill(stdout)

        self.assertEqual(b"\"memcached://localhost:11215\";",
                         env[b"export FOOBAR_URL"])
        self.assertEqual(b"\"memcached://localhost:11215\";",
                         env[b"export FOOBAR_MEMCACHED_URL"])
        self.assertEqual(env[b"export PIFPAF_PID"],
                         env[b"export FOOBAR_PID"])

    @testtools.skipUnless(spawn.find_executable("memcached"),
                          "memcached not found")
    def test_global_urls_varibale(self):
        c = subprocess.Popen(["pifpaf", "run",
                              "--env-prefix", "FOOBAR",
                              "memcached", "--port", "11217",
                              "--",
                              "pifpaf",
                              "run", "memcached", "--port", "11218"],
                             bufsize=0,
                             stdout=subprocess.PIPE)
        (stdout, stderr) = c.communicate()
        self.assertEqual(0, c.wait())
        env = self._read_stdout_and_kill(stdout)

        self.assertEqual(b"\"memcached://localhost:11218\";",
                         env[b"export PIFPAF_URL"])
        self.assertEqual(b"\"memcached://localhost:11218\";",
                         env[b"export PIFPAF_MEMCACHED_URL"])
        self.assertEqual(
            b"\"memcached://localhost:11217;memcached://localhost:11218\";",
            env[b"export PIFPAF_URLS"])

    @testtools.skipUnless(spawn.find_executable("memcached"),
                          "memcached not found")
    def test_global_urls_varibale_old_format(self):
        c = subprocess.Popen(["pifpaf",
                              "--env-prefix", "FOOBAR",
                              "run", "memcached", "--port", "11217",
                              "--",
                              "pifpaf",
                              "run", "memcached", "--port", "11218"],
                             bufsize=0,
                             stdout=subprocess.PIPE)
        (stdout, stderr) = c.communicate()
        self.assertEqual(0, c.wait())
        env = self._read_stdout_and_kill(stdout)

        self.assertEqual(b"\"memcached://localhost:11218\";",
                         env[b"export PIFPAF_URL"])
        self.assertEqual(b"\"memcached://localhost:11218\";",
                         env[b"export PIFPAF_MEMCACHED_URL"])
        self.assertEqual(
            b"\"memcached://localhost:11217;memcached://localhost:11218\";",
            env[b"export PIFPAF_URLS"])
