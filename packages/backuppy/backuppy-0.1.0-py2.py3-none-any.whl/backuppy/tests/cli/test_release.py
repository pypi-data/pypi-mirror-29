from unittest import TestCase

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from backuppy.cli.release import main


class CliTest(TestCase):
    def test_without_semantic_version(self):
        args = ['--version', 'foo']
        with self.assertRaises(ValueError):
            main(args)

    def test_without_arguments(self):
        args = []
        with self.assertRaises(SystemExit):
            main(args)

    @patch('subprocess.call')
    def test(self, m):
        args = ['--version', '0.0.0']
        main(args)
