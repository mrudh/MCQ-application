import unittest
from unittest.mock import mock_open, patch
import assessment_storage


class TestAssessmentStorage_Branches(unittest.TestCase):

    #Tests load_custom_assessments returns an empty list when the storage file does not exist
    @patch("assessment_storage.os.path.exists", return_value=False)
    def test_load_custom_assessments_no_file(self, m_exists):
        self.assertEqual(assessment_storage.load_custom_assessments(), [])


    #Tests load_custom_assessments reads and returns JSON content when the storage file exists
    @patch("assessment_storage.os.path.exists", return_value=True)
    @patch("assessment_storage.open",
        new_callable=mock_open,
        read_data='[{"name":"A"}]',
    )
    def test_load_custom_assessments_with_file(self, m_open, m_exists):
        self.assertEqual(assessment_storage.load_custom_assessments(), [{"name": "A"}])


    #Verifies save_custom_assessments opens the file for writing and attempts to write JSON
    @patch("assessment_storage.open", new_callable=mock_open)
    def test_save_custom_assessments_writes_file(self, m_open):
        assessment_storage.save_custom_assessments([{"name": "A"}])
        m_open.assert_called_once()


if __name__ == "__main__":
    unittest.main()