import unittest
from unittest.mock import patch, MagicMock
import logging
import textwrap

# Import the functions under test
from backend.database.postgres import (
    create_user,
    get_user_by_id,
    update_user_email,
    delete_user
    # Add other functions here as needed
)

class TestPostgreCrudOps(unittest.TestCase):

    # ------------------------
    # Tests for create_user
    # ------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_create_user_success(self, mock_get_db_connection):
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Call the function under test
        result = create_user('user_123', 'johndoe', 'john.doe@example.com')

        # Assertions
        self.assertTrue(result)
        mock_get_db_connection.assert_called_once()

        query_str = """
            INSERT INTO users (id, username, email)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """
        mock_cursor.execute.assert_called_once_with(query_str, ('user_123', 'johndoe', 'john.doe@example.com'))
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_create_user_db_connection_failure(self, mock_get_db_connection):
        # Mock get_db_connection to return None
        mock_get_db_connection.return_value = None

        # Call the function under test
        result = create_user('user_123', 'johndoe', 'john.doe@example.com')

        # Assertions
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_create_user_exception(self, mock_get_db_connection):
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception('Database error')
        mock_get_db_connection.return_value = mock_conn

        # Call the function under test
        result = create_user('user_123', 'johndoe', 'john.doe@example.com')

        # Assertions
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()
        mock_conn.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    # ------------------------
    # Tests for get_user_by_id
    # ------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_get_user_by_id_success(self, mock_get_db_connection):
        # Mock result
        mock_user = {'id': 'user_123', 'username': 'johndoe', 'email': 'john.doe@example.com'}

        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        mock_cursor.fetchone.return_value = mock_user

        # Call the function under test
        result = get_user_by_id('user_123')

        # Assertions
        self.assertEqual(result, mock_user)
        mock_get_db_connection.assert_called_once()
        mock_cursor.execute.assert_called_once_with("SELECT * FROM users WHERE id = %s;", ('user_123',))
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_get_user_by_id_no_user(self, mock_get_db_connection):
        # Mock no result
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None
        mock_get_db_connection.return_value = mock_conn

        # Call the function under test
        result = get_user_by_id('nonexistent_user')

        # Assertions
        self.assertIsNone(result)
        mock_get_db_connection.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_get_user_by_id_exception(self, mock_get_db_connection):
        # Mock an exception
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception('Database query error')
        mock_get_db_connection.return_value = mock_conn

        # Call the function under test
        result = get_user_by_id('user_123')

        # Assertions
        self.assertIsNone(result)
        mock_get_db_connection.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    # ------------------------
    # Tests for update_user_email
    # ------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_update_user_email_success(self, mock_get_db_connection):
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Simulate success by not raising exceptions
        result = update_user_email('user_123', 'new_email@example.com')

        # Assertions
        self.assertTrue(result)
        mock_get_db_connection.assert_called_once()
        mock_cursor.execute.assert_called_once_with("UPDATE users SET email = %s WHERE id = %s;", ('new_email@example.com', 'user_123'))
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_update_user_email_db_connection_failure(self, mock_get_db_connection):
        # Mock get_db_connection to return None
        mock_get_db_connection.return_value = None

        # Call the function
        result = update_user_email('user_123', 'new_email@example.com')

        # Assertions
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_update_user_email_exception(self, mock_get_db_connection):
        # Mock an exception on execute
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Update error')
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = update_user_email('user_123', 'new_email@example.com')

        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()
        mock_conn.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    # ------------------------
    # Tests for delete_user
    # ------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_delete_user_success(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Simulate success by not raising exceptions
        result = delete_user('user_123')

        self.assertTrue(result)
        mock_get_db_connection.assert_called_once()
        mock_cursor.execute.assert_called_once_with("DELETE FROM users WHERE id = %s;", ('user_123',))
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_delete_user_db_connection_failure(self, mock_get_db_connection):
        # Mock get_db_connection to return None
        mock_get_db_connection.return_value = None

        result = delete_user('user_123')
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_delete_user_exception(self, mock_get_db_connection):
        # Mock an exception on execute
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Delete error')
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = delete_user('user_123')
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()
        mock_conn.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()