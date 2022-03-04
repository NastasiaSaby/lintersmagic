"""
Run under IPython with `ipython tests/test_.*py`.

The unittest discovery with `python -m unittest discover -s tests`, or what I imagine to be the IPython version `ipython -m unittest discover -s tests` is not working, for some reason, and is complaining about `get_ipython()` not being in the context.
"""
import unittest
import logging
from lintersmagic import pycodestyle, pycodestyle_on, vw

class TestLinenumbers(unittest.TestCase):

    def test_pycodestyle_reports_correct_linenumber(self):
        """Test that pycodestyle reports correct line numbers, and
        accommodates for the cell magic at the top of the cell which is takes
        one line.
        """
        cell = '''print( "oh look kittens!" )'''
        with self.assertLogs() as captured:
            pycodestyle(None, cell)
        self.assertEqual(len(captured.records), 2)  # check that there is only one log message
        self.assertEqual(captured.records[0].getMessage(), "2:7: E201 whitespace after '('")
        self.assertEqual(captured.records[1].getMessage(), "2:26: E202 whitespace before ')'")

    def test_pycodestyle_reports_correct_linenumber_with_leading_empty_lines(self):
        """Test that pycodestyle reports the correct line numbers when there
        are empty lines at the top of the cell, after the cell magic
        but before the actual code.
        """
        cell = '''\nprint( "oh look kittens!" )'''
        with self.assertLogs() as captured:
            pycodestyle(None, cell)
            self.assertEqual(len(captured.records), 2)
            self.assertEqual(captured.records[0].getMessage(), "3:7: E201 whitespace after '('")
            self.assertEqual(captured.records[1].getMessage(), "3:26: E202 whitespace before ')'")

    def test_pycodestyle_reports_three_leading_empty_lines(self):
        """Test that pycodestyle still reports if there are too many empty
        lines at the beginning of the cell.
        """
        cell = '''\n\n\nprint("this is fine")'''
        with self.assertLogs() as captured:
            pycodestyle(None, cell)
            self.assertEqual(len(captured.records), 1)
            self.assertEqual(captured.records[0].getMessage(), "5:1: E303 too many blank lines (3)")

    def test_pycodestyle_leading_comments_skipped_when_reporting(self):
        """Test that leading comments lines are skipped when pycodestyle does
report style issues.
        """
        cell = '''# a comment line\nprint( "oh look kittens!" )'''
        with self.assertLogs() as captured:
            pycodestyle(None, cell)
            self.assertEqual(len(captured.records), 2)
            self.assertEqual(captured.records[0].getMessage(), "3:7: E201 whitespace after '('")
            self.assertEqual(captured.records[1].getMessage(), "3:26: E202 whitespace before ')'")

    def test_pycodestyle_line_too_long(self):
        """Test that leading comments lines are skipped when pycodestyle does
report style issues.
        """
        cell = '''aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'''
        with self.assertLogs() as captured:
            pycodestyle(None, cell)
            self.assertEqual(len(captured.records), 1)
            self.assertEqual(captured.records[0].getMessage(), "2:80: E501 line too long (80 > 79 characters)")

#     def test_pycodestyle_skip_line_too_long(self):
#         """Test that leading comments lines are skipped when pycodestyle does
# report style issues.
#         """
#         line = ''' --ignore E501'''
#         next_cell = '''aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'''
#         with self.assertLogs() as captured:
#             pycodestyle_on(line)
#             # pycodestyle(None, next_cell)
#             self.assertEqual(len(captured.records), 4)
#             self.assertEqual(captured.records[0].getMessage(), "2:80: E501 line too long (80 > 79 characters)")

if __name__ == '__main__':
    unittest.main()
