import unittest
from unittest.mock import patch, MagicMock

# Import the functions under test
from backend.database.vectorDelete import delete_embedding_by_title, delete_embedding_by_id

class TestDeleteEmbedding(unittest.TestCase):

    @patch('backend.database.vectorDelete.get_db_connection')
    def test_delete_embedding_by_title_success(self, mock_get_db_connection):
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Configure cursor.rowcount to simulate a successful deletion
        mock_cursor.rowcount = 1

        # Call the function under test
        title = "Insert 1"
        result = delete_embedding_by_title(title)

        # Assertions
        self.assertTrue(result)
        mock_cursor.execute.assert_called_once_with(
            """
                DELETE FROM course_materials
                WHERE title = %s;
            """,
            (title,)
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch('backend.database.vectorDelete.get_db_connection')
    def test_delete_embedding_by_title_no_record_found(self, mock_get_db_connection):
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Configure cursor.rowcount to simulate no records deleted
        mock_cursor.rowcount = 0

        # Call the function under test
        title = "Nonexistent Title"
        result = delete_embedding_by_title(title)

        # Assertions
        self.assertFalse(result)
        mock_cursor.execute.assert_called_once_with(
            """
                DELETE FROM course_materials
                WHERE title = %s;
            """,
            (title,)
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch('backend.database.vectorDelete.get_db_connection')
    def test_delete_embedding_by_title_db_connection_failure(self, mock_get_db_connection):
        # Mock get_db_connection to return None
        mock_get_db_connection.return_value = None

        # Call the function under test
        title = "Insert 1"
        result = delete_embedding_by_title(title)

        # Assertions
        self.assertFalse(result)

    @patch('backend.database.vectorDelete.get_db_connection')
    def test_delete_embedding_by_title_exception(self, mock_get_db_connection):
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Configure cursor.execute to raise an exception
        mock_cursor.execute.side_effect = Exception('Database error')

        # Call the function under test
        title = "Insert 1"
        result = delete_embedding_by_title(title)

        # Assertions
        self.assertFalse(result)
        mock_conn.rollback.assert_called_once()
        mock_conn.close.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch('backend.database.vectorDelete.get_db_connection')
    def test_delete_embedding_by_id_success(self, mock_get_db_connection):
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Configure cursor.rowcount to simulate a successful deletion
        mock_cursor.rowcount = 1

        # Call the function under test
        record_id = 1
        result = delete_embedding_by_id(record_id)

        # Assertions
        self.assertTrue(result)
        mock_cursor.execute.assert_called_once_with(
            """
                DELETE FROM course_materials
                WHERE id = %s;
            """,
            (record_id,)
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch('backend.database.vectorDelete.get_db_connection')
    def test_delete_embedding_by_id_no_record_found(self, mock_get_db_connection):
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Configure cursor.rowcount to simulate no records deleted
        mock_cursor.rowcount = 0

        # Call the function under test
        record_id = 9999  # Assuming this ID does not exist
        result = delete_embedding_by_id(record_id)

        # Assertions
        self.assertFalse(result)
        mock_cursor.execute.assert_called_once_with(
            """
                DELETE FROM course_materials
                WHERE id = %s;
            """,
            (record_id,)
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch('backend.database.vectorDelete.get_db_connection')
    def test_delete_embedding_by_id_db_connection_failure(self, mock_get_db_connection):
        # Mock get_db_connection to return None
        mock_get_db_connection.return_value = None

        # Call the function under test
        record_id = 1
        result = delete_embedding_by_id(record_id)

        # Assertions
        self.assertFalse(result)

    @patch('backend.database.vectorDelete.get_db_connection')
    def test_delete_embedding_by_id_exception(self, mock_get_db_connection):
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Configure cursor.execute to raise an exception
        mock_cursor.execute.side_effect = Exception('Database error')

        # Call the function under test
        record_id = 1
        result = delete_embedding_by_id(record_id)

        # Assertions
        self.assertFalse(result)
        mock_conn.rollback.assert_called_once()
        mock_conn.close.assert_called_once()
        mock_cursor.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()