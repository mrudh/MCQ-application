import sys
import types
import unittest
from unittest.mock import patch
import mcq


class TestTimedQuizFromTSLFrames(unittest.TestCase):
    PROMPT = "Enter choice: "


    @staticmethod
    def _install_fake_msvcrt(kbhit_sequence, getwch_sequence):
        fake = types.ModuleType("msvcrt")
        kbhit_iter = iter(kbhit_sequence)
        getwch_iter = iter(getwch_sequence)

        def kbhit():
            return next(kbhit_iter)

        def getwch():
            return next(getwch_iter)

        fake.kbhit = kbhit
        fake.getwch = getwch
        sys.modules["msvcrt"] = fake


    @patch("builtins.print")
    @patch("select.select", side_effect=ValueError("timeout must be non-negative"))
    def test_frame_1_negative_timeout_unix_like_raises(
        self,
        _mock_select,
        _mock_print,
    ):
        with patch("mcq.sys.platform", "linux"):
            with self.assertRaises(ValueError):
                mcq.timed_quiz(self.PROMPT, timeout=-1)


    @patch("builtins.print")
    @patch("mcq.time.sleep", return_value=None)
    def test_frame_8_windows_zero_enter_pressed_returns_uppercase(
            self,
            _mock_sleep,
            _mock_print,
    ):
        self._install_fake_msvcrt(
            kbhit_sequence=[True, True, True],
            getwch_sequence=["a", "b", "\r"],
        )
        with patch("mcq.sys.platform", "win32"):
            with patch("mcq.time.time", side_effect=[0.0, 0.1, 0.2, 0.3]):
                result = mcq.timed_quiz(self.PROMPT, timeout=1)
        self.assertEqual(result, "AB")


    @patch("builtins.print")
    @patch("mcq.time.sleep", return_value=None)
    def test_frame_9_windows_zero_backspace_used_edits_buffer(
            self,
            _mock_sleep,
            _mock_print,
    ):
        self._install_fake_msvcrt(
            kbhit_sequence=[True, True, True, True, True],
            getwch_sequence=["a", "b", "\b", "c", "\r"],
        )
        with patch("mcq.sys.platform", "win32"):
            with patch("mcq.time.time", side_effect=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5]):
                result = mcq.timed_quiz(self.PROMPT, timeout=1)
        self.assertEqual(result, "AC")


    @patch("builtins.print")
    @patch("mcq.time.sleep", return_value=None)
    def test_frame_10_windows_zero_typed_chars_enter_returns_uppercase(
            self,
            _mock_sleep,
            _mock_print,
    ):
        self._install_fake_msvcrt(
            kbhit_sequence=[True, True, True, True],
            getwch_sequence=["x", "y", "z", "\r"],
        )
        with patch("mcq.sys.platform", "win32"):
            with patch("mcq.time.time", side_effect=[0.0, 0.1, 0.2, 0.3, 0.4]):
                result = mcq.timed_quiz(self.PROMPT, timeout=1)
        self.assertEqual(result, "XYZ")


    @patch("builtins.print")
    @patch("mcq.time.sleep", return_value=None)
    def test_frame_11_windows_zero_no_input_returns_none(
        self,
        _mock_sleep,
        _mock_print,
    ):
        self._install_fake_msvcrt(
            kbhit_sequence=[False],
            getwch_sequence=[],
        )
        with patch("mcq.sys.platform", "win32"):
            with patch("mcq.time.time", side_effect=[0.0, 0.0, 0.1]):
                result = mcq.timed_quiz(self.PROMPT, timeout=0)
        self.assertIsNone(result)


    @patch("builtins.print")
    @patch("mcq.time.sleep", return_value=None)
    def test_frame_12_windows_positive_enter_pressed_returns_uppercase(
        self,
        _mock_sleep,
        _mock_print,
    ):
        self._install_fake_msvcrt(
            kbhit_sequence=[True, True, True],
            getwch_sequence=["c", "d", "\r"],
        )
        with patch("mcq.sys.platform", "win32"):
            with patch("mcq.time.time", side_effect=[0.0, 0.1, 0.2, 0.3]):
                result = mcq.timed_quiz(self.PROMPT, timeout=5)
        self.assertEqual(result, "CD")


    @patch("builtins.print")
    @patch("mcq.time.sleep", return_value=None)
    def test_frame_15_windows_positive_no_input_returns_none(
        self,
        _mock_sleep,
        _mock_print,
    ):
        self._install_fake_msvcrt(
            kbhit_sequence=[False, False, False],
            getwch_sequence=[],
        )
        with patch("mcq.sys.platform", "win32"):
            with patch("mcq.time.time", side_effect=[0.0, 10.0, 10.1]):
                result = mcq.timed_quiz(self.PROMPT, timeout=5)
        self.assertIsNone(result)


    @patch("builtins.print")
    @patch("select.select", return_value=([sys.stdin], [], []))
    def test_frame_16_unix_zero_available_returns_uppercase(
        self,
        _mock_select,
        _mock_print,
    ):
        with patch("mcq.sys.platform", "darwin"):
            with patch("mcq.sys.stdin.readline", return_value="ab\n"):
                result = mcq.timed_quiz(self.PROMPT, timeout=0)
        self.assertEqual(result, "AB")


    @patch("builtins.print")
    @patch("select.select", return_value=([], [], []))
    def test_frame_17_unix_zero_not_available_returns_none(
        self,
        _mock_select,
        _mock_print,
    ):
        with patch("mcq.sys.platform", "linux"):
            result = mcq.timed_quiz(self.PROMPT, timeout=0)
        self.assertIsNone(result)


    @patch("builtins.print")
    @patch("select.select", return_value=([sys.stdin], [], []))
    def test_frame_18_unix_positive_available_returns_uppercase(
        self,
        _mock_select,
        _mock_print,
    ):
        with patch("mcq.sys.platform", "linux"):
            with patch("mcq.sys.stdin.readline", return_value="xYz\n"):
                result = mcq.timed_quiz(self.PROMPT, timeout=5)
        self.assertEqual(result, "XYZ")


    @patch("builtins.print")
    @patch("select.select", return_value=([], [], []))
    def test_frame_19_unix_positive_not_available_returns_none(
        self,
        _mock_select,
        _mock_print,
    ):
        with patch("mcq.sys.platform", "darwin"):
            result = mcq.timed_quiz(self.PROMPT, timeout=5)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
