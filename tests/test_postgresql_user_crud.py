import unittest
from unittest.mock import patch, MagicMock
import logging
import textwrap

# Import the functions under test
from backend.database.postgres import (
    create_user,
    read_user_by_id,
    read_user_by_email,
    update_user_email,
    delete_user
    # Add other functions here as needed
)

class TestUserCrudOps(unittest.TestCase):

    # ------------------------------------------------------------------
    # Tests for create_user
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_create_user_success(self, mock_get_db_connection):
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Call the function under test
        result = create_user(display_name='Alice', email='alice@example.com', role='professor')

        # Assertions
        self.assertTrue(result)
        mock_get_db_connection.assert_called_once()

        # Verify the query and parameters
        expected_query = """
            INSERT INTO users (display_name, email, role)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """
        mock_cursor.execute.assert_called_once_with(
            expected_query,
            ('Alice', 'alice@example.com', 'professor')
        )
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_create_user_db_connection_failure(self, mock_get_db_connection):
        # Mock get_db_connection to return None
        mock_get_db_connection.return_value = None

        # Call the function under test
        result = create_user('Bob', 'bob@example.com')

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
        result = create_user('Charlie', 'charlie@example.com', 'student')

        # Assertions
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()
        mock_conn.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    # ------------------------------------------------------------------
    # Tests for read_user_by_id
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_read_user_by_id_success(self, mock_get_db_connection):
        # Mock row: The function only returns 'display_name'
        mock_row = {'display_name': 'Alice'}

        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = mock_row
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Call the function
        result = read_user_by_id('some-uuid-123')

        # Assertions
        self.assertEqual(result, 'Alice')  # Only the display_name is returned
        mock_get_db_connection.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "SELECT display_name FROM users WHERE id = %s;", 
            ('some-uuid-123',)
        )
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_read_user_by_id_no_user(self, mock_get_db_connection):
        # Mock no result
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Call the function
        result = read_user_by_id('nonexistent-uuid')

        # Assertions
        self.assertIsNone(result)
        mock_get_db_connection.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_read_user_by_id_exception(self, mock_get_db_connection):
        # Mock exception
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Query error')
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = read_user_by_id('some-uuid-123')
        self.assertIsNone(result)
        mock_get_db_connection.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    # ------------------------------------------------------------------
    # Tests for read_user_by_email
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_read_user_by_email_success(self, mock_get_db_connection):
        # Mock row
        mock_row = {'display_name': 'Bob'}

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = mock_row
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = read_user_by_email('bob@example.com')
        self.assertEqual(result, 'Bob')
        mock_get_db_connection.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "SELECT display_name FROM users WHERE email = %s;",
            ('bob@example.com',)
        )
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_read_user_by_email_no_user(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = read_user_by_email('unknown@example.com')
        self.assertIsNone(result)
        mock_get_db_connection.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_read_user_by_email_exception(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Query error')
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = read_user_by_email('charlie@example.com')
        self.assertIsNone(result)
        mock_get_db_connection.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    # ------------------------------------------------------------------
    # Tests for update_user_email
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_update_user_email_success(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Simulate success by not raising exceptions
        result = update_user_email('Alice', 'alice.new@example.com')

        self.assertTrue(result)
        mock_get_db_connection.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "UPDATE users SET email = %s WHERE display_name = %s;",
            ('alice.new@example.com', 'Alice')
        )
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_update_user_email_db_connection_failure(self, mock_get_db_connection):
        mock_get_db_connection.return_value = None

        result = update_user_email('Bob', 'bob.new@example.com')
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_update_user_email_exception(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Update error')
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = update_user_email('Bob', 'bob.new@example.com')
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()
        mock_conn.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    # ------------------------------------------------------------------
    # Tests for delete_user
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_delete_user_success(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = delete_user('some-uuid-123')

        self.assertTrue(result)
        mock_get_db_connection.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "DELETE FROM users WHERE id = %s;", 
            ('some-uuid-123',)
        )
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_delete_user_db_connection_failure(self, mock_get_db_connection):
        mock_get_db_connection.return_value = None

        result = delete_user('some-uuid-123')
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_delete_user_exception(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Delete error')
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = delete_user('some-uuid-123')
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()
        mock_conn.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()