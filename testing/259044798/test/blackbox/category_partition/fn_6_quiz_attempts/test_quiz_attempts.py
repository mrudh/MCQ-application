import os
import json
import tempfile
import unittest
import attempts as qa


class TestQuizAttemptsFrames(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.attempt_file = os.path.join(self.tmpdir.name, "attempts.json")
        qa.ATTEMPT_FILE = self.attempt_file
        self.default_max = qa.MAX_ATTEMPTS_PER_DAY

    def tearDown(self):
        self.tmpdir.cleanup()

    def _make_file_exist_with_valid_json(self, data=None):
        if data is None:
            data = {}
        with open(self.attempt_file, "w", encoding="utf-8") as f:
            json.dump(data, f)


    def test_1_1_1_1_get_empty_missing(self):
        if os.path.exists(self.attempt_file):
            os.remove(self.attempt_file)
        remaining = qa.get_attempts_left("   ")  
        self.assertEqual(self.default_max, remaining)

   
    def test_1_1_2_1_get_empty_exists(self):
        self._make_file_exist_with_valid_json({})
        remaining = qa.get_attempts_left("   ") 
        self.assertEqual(self.default_max, remaining)

   
    def test_1_2_1_1_get_nonempty_missing(self):
        if os.path.exists(self.attempt_file):
            os.remove(self.attempt_file)
        remaining = qa.get_attempts_left("Devyani")
        self.assertEqual(self.default_max, remaining)

    
    def test_1_2_2_1_get_nonempty_exists(self):
        self._make_file_exist_with_valid_json({})
        remaining = qa.get_attempts_left("Devyani")
        self.assertEqual(self.default_max, remaining)

    
    def test_2_1_1_2_can_empty_missing(self):
        if os.path.exists(self.attempt_file):
            os.remove(self.attempt_file)
        can, remaining = qa.can_attempt_quiz("   ")
        self.assertTrue(can)
        self.assertEqual(self.default_max, remaining)


    def test_2_1_2_2_can_empty_exists(self):
        self._make_file_exist_with_valid_json({})
        can, remaining = qa.can_attempt_quiz("   ")
        self.assertTrue(can)
        self.assertEqual(self.default_max, remaining)

   
    def test_2_2_1_2_can_nonempty_missing(self):
        if os.path.exists(self.attempt_file):
            os.remove(self.attempt_file)
        can, remaining = qa.can_attempt_quiz("Devyani")
        self.assertTrue(can)
        self.assertEqual(self.default_max, remaining)

    
    def test_2_2_2_2_can_nonempty_exists(self):
        self._make_file_exist_with_valid_json({})
        can, remaining = qa.can_attempt_quiz("Devyani")
        self.assertTrue(can)
        self.assertEqual(self.default_max, remaining)


if __name__ == "__main__":
    unittest.main()
