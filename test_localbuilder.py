#!/usr/bin/env python

import sys
import unittest
import commands
import StringIO

from localbuilder import run_if_changes, get_changed_files

class CITests(unittest.TestCase):

    def setUp(self):
        self.old_value_of_stdout = sys.stdout
        sys.stdout = StringIO.StringIO()
    def tearDown(self):
        sys.stdout = self.old_value_of_stdout
        
    def assert_equal(self, *args, **kwargs):
        "Assert that two values are equal"
        return self.assertEqual(*args, **kwargs)      

    def assert_not_equal(self, *args, **kwargs):
        "Assert that two values are not equal"
        return not self.assertEqual(*args, **kwargs)

    def test_get_changed_files(self):
        outcome = get_changed_files('.',0)
        self.assert_equal([], outcome)

    def test_get_changed_files(self):
        outcome = get_changed_files('.',0)
        self.assert_equal([], outcome)

    def test_get_changed_files_gets_correct_output(self):
        commands.getoutput("mkdir testdir1234")
        commands.getoutput("touch testdir1234/testfile1234")
        outcome = get_changed_files('testdir1234', 1)
        self.assert_equal(1, len(outcome))
        self.assert_equal(['testdir1234/testfile1234'], outcome)
        commands.getoutput("rm testdir1234/testfile1234")
        commands.getoutput("rmdir testdir1234")

    def test_run_if_changes_does_nothing_with_blank_list(self):
        empty_list = []
        outcome = run_if_changes(empty_list, "ls")
        self.assert_equal(False, outcome)

    def test_run_if_changes_runs_command_with_list(self):
        empty_list = [1,]
        command_to_run = "ls"
        expected = commands.getoutput(command_to_run)
        outcome = run_if_changes(empty_list, command_to_run)
        self.assert_equal(expected, outcome)        
        
if __name__ == "__main__":
    unittest.main()