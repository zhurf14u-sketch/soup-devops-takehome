import io
import json
import unittest
from contextlib import redirect_stdout

from soup_cli import __version__
from soup_cli.cli import main


class CliTests(unittest.TestCase):
    def test_json_output_is_stable(self):
        stream = io.StringIO()
        with redirect_stdout(stream):
            exit_code = main(["--json"])
        self.assertEqual(exit_code, 0)
        payload = json.loads(stream.getvalue())
        self.assertEqual(payload["package"], "soup-release-demo")
        self.assertEqual(payload["version"], __version__)


if __name__ == "__main__":
    unittest.main()
