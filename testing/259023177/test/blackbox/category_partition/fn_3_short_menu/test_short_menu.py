import unittest
from unittest.mock import patch
import importlib



MODULE_UNDER_TEST = "main"


def _import_target():
    return importlib.import_module(MODULE_UNDER_TEST)


class TestMenuSystem_FromTSLFrames_First20(unittest.TestCase):
    def setUp(self):
        self.t = _import_target()

        
        self.sample_data = [
            {"question": "Q1", "options": ["A. a", "B. b", "C. c", "D. d"], "answer": "A"},
            {"question": "Q2", "options": ["A. a2", "B. b2", "C. c2", "D. d2"], "answer": "B"},
        ]

    def _patch_common_quiz_data(self):
        return patch.object(self.t, "ALL_QUIZ_DATA", self.sample_data, create=True)


    def _patch_random_sample(self):
        return patch("random.sample", side_effect=lambda data, n: data[:n])


    def _run_timed_quiz_via_quiz_modes(self, name_input, num_input):
        with self._patch_common_quiz_data(), self._patch_random_sample():
            with patch.object(self.t, "take_quiz", create=True) as take_quiz_mock:
                inputs = ["1", name_input, num_input, "0"]
                with patch("builtins.input", side_effect=inputs):
                    self.t.quiz_modes_menu()
                return take_quiz_mock

    def test_frame_1_quick_to_timed_name_provided_num_valid(self):
        take_quiz_mock = self._run_timed_quiz_via_quiz_modes("Sarthak", "1")
        self.assertTrue(take_quiz_mock.called)
        args, kwargs = take_quiz_mock.call_args
        self.assertTrue(kwargs.get("timed", False))
        self.assertEqual(args[3], "Sarthak")  
        self.assertEqual(len(args[0]), 1)

    def test_frame_2_quick_to_timed_name_provided_num_invalid(self):
        take_quiz_mock = self._run_timed_quiz_via_quiz_modes("Sarthak", "abc")
        args, kwargs = take_quiz_mock.call_args
        self.assertTrue(kwargs.get("timed", False))
        self.assertEqual(args[3], "Sarthak") 
        self.assertEqual(len(args[0]), len(self.sample_data))

    def test_frame_3_quick_to_timed_name_empty_num_valid(self):
        take_quiz_mock = self._run_timed_quiz_via_quiz_modes("", "1")
        args, kwargs = take_quiz_mock.call_args
        self.assertTrue(kwargs.get("timed", False))
        self.assertEqual(args[3], "")  
        self.assertEqual(len(args[0]), 1)

    def test_frame_4_quick_to_timed_name_empty_num_invalid(self):
        take_quiz_mock = self._run_timed_quiz_via_quiz_modes("", "abc")
        args, kwargs = take_quiz_mock.call_args
        self.assertTrue(kwargs.get("timed", False))
        self.assertEqual(args[3], "") 
        self.assertEqual(len(args[0]), len(self.sample_data))

    
    def _run_fifty_fifty_via_quiz_modes(self, name_input, num_input):
        with self._patch_common_quiz_data(), self._patch_random_sample():
            with patch.object(self.t, "fifty_fifty_quiz", create=True) as ff_mock:
                inputs = ["5", name_input, num_input, "0"]
                with patch("builtins.input", side_effect=inputs):
                    self.t.quiz_modes_menu()
                return ff_mock

    def test_frame_5_quick_to_5050_name_provided_num_valid(self):
        ff_mock = self._run_fifty_fifty_via_quiz_modes("Sarthak", "1")
        self.assertTrue(ff_mock.called)
        args, _ = ff_mock.call_args
        self.assertEqual(args[3], "Sarthak")
        self.assertEqual(len(args[0]), 1)

    def test_frame_6_quick_to_5050_name_provided_num_invalid(self):
        ff_mock = self._run_fifty_fifty_via_quiz_modes("Sarthak", "abc")
        args, _ = ff_mock.call_args
        self.assertEqual(args[3], "Sarthak")
        self.assertEqual(len(args[0]), len(self.sample_data))

    def test_frame_7_quick_to_5050_name_empty_num_valid(self):
        ff_mock = self._run_fifty_fifty_via_quiz_modes("", "1")
        args, _ = ff_mock.call_args
        self.assertEqual(args[3], "")
        self.assertEqual(len(args[0]), 1)

    def test_frame_8_quick_to_5050_name_empty_num_invalid(self):
        ff_mock = self._run_fifty_fifty_via_quiz_modes("", "abc")
        args, _ = ff_mock.call_args
        self.assertEqual(args[3], "")
        self.assertEqual(len(args[0]), len(self.sample_data))

    
    def _run_quiz_modes_back_only(self):
        with patch("builtins.input", side_effect=["0"]):
            self.t.quiz_modes_menu()

    def test_frame_9_quiz_modes_back(self):
        self._run_quiz_modes_back_only()

    def test_frame_10_quiz_modes_back(self):
        self._run_quiz_modes_back_only()

    def test_frame_11_quiz_modes_back(self):
        self._run_quiz_modes_back_only()

    def test_frame_12_quiz_modes_back(self):
        self._run_quiz_modes_back_only()

    
    def _run_assessments_create_then_back(self):
        with patch.object(self.t, "create_assessment", create=True) as create_mock:
            with patch("builtins.input", side_effect=["1", "0"]):
                self.t.assessments_menu()
            return create_mock

    def test_frame_13_assessments_create(self):
        self.assertTrue(self._run_assessments_create_then_back().called)

    def test_frame_14_assessments_create(self):
        self.assertTrue(self._run_assessments_create_then_back().called)

    def test_frame_15_assessments_create(self):
        self.assertTrue(self._run_assessments_create_then_back().called)

    def test_frame_16_assessments_create(self):
        self.assertTrue(self._run_assessments_create_then_back().called)

    
    def _run_assessments_open_then_back(self):
        with patch.object(self.t, "open_assessment", create=True) as open_mock:
            with patch("builtins.input", side_effect=["6", "0"]):
                self.t.assessments_menu()
            return open_mock

    def test_frame_17_assessments_open(self):
        self.assertTrue(self._run_assessments_open_then_back().called)

    def test_frame_18_assessments_open(self):
        self.assertTrue(self._run_assessments_open_then_back().called)

    def test_frame_19_assessments_open(self):
        self.assertTrue(self._run_assessments_open_then_back().called)

    def test_frame_20_assessments_open(self):
        self.assertTrue(self._run_assessments_open_then_back().called)


if __name__ == "__main__":
    unittest.main(verbosity=2)
