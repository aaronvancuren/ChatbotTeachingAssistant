import unittest
from unittest.mock import patch, MagicMock

# Import the functions under test
from backend.database.postgres import (
    create_user,
    read_user_by_id,
    read_user_by_email,
    read_email_by_id,
    update_user_display_name,
    delete_user
)

class TestUserCrudOps(unittest.TestCase):

    # ------------------------------------------------------------------
    # Tests for create_user
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_create_user_success(self, mock_get_db_connection):
        """Test creating a user successfully."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = create_user(display_name='Alice', email='alice@example.com', role='professor')
        self.assertTrue(result)

        mock_get_db_connection.assert_called_once()

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

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_create_user_db_connection_failure(self, mock_get_db_connection, mock_log_error):
        """Test when get_db_connection returns None."""
        mock_get_db_connection.return_value = None

        result = create_user('Bob', 'bob@example.com')
        self.assertFalse(result)

        mock_get_db_connection.assert_called_once()
        mock_log_error.assert_called_once_with("Failed to connect to the database.")

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_create_user_exception(self, mock_get_db_connection, mock_log_error):
        """Test exception during INSERT query."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Database error')
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = create_user('Charlie', 'charlie@example.com', 'student')
        self.assertFalse(result)

        mock_get_db_connection.assert_called_once()
        mock_conn.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

        mock_log_error.assert_called_once_with("Error inserting user: Database error")

    # ------------------------------------------------------------------
    # Tests for read_user_by_id
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_read_user_by_id_success(self, mock_get_db_connection):
        """Test retrieving user info (display_name, role) by ID."""
        mock_row = {'display_name': 'Alice', 'role': 'student'}
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = mock_row
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = read_user_by_id('some-uuid-123')
        self.assertEqual(result, mock_row)

        mock_get_db_connection.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "SELECT display_name, role FROM users WHERE id = %s;", 
            ('some-uuid-123',)
        )
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_read_user_by_id_no_user(self, mock_get_db_connection):
        """Test returning None if no user found."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = read_user_by_id('nonexistent-uuid')
        self.assertIsNone(result)

        mock_get_db_connection.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_read_user_by_id_exception(self, mock_get_db_connection, mock_log_error):
        """Test exception handling for read_user_by_id."""
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

        mock_log_error.assert_called_once_with("Error retrieving user: Query error")

    # ------------------------------------------------------------------
    # Tests for read_user_by_email
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_read_user_by_email_success(self, mock_get_db_connection):
        """Test retrieving user info (display_name, role) by email."""
        mock_row = {'display_name': 'Bob', 'role': 'student'}
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = mock_row
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = read_user_by_email('bob@example.com')
        self.assertEqual(result, mock_row)

        mock_get_db_connection.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "SELECT display_name, role FROM users WHERE email = %s;",
            ('bob@example.com',)
        )
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_read_user_by_email_no_user(self, mock_get_db_connection):
        """Test returning None if no user found by email."""
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

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_read_user_by_email_exception(self, mock_get_db_connection, mock_log_error):
        """Test exception when reading user by email."""
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

        mock_log_error.assert_called_once_with("Error retrieving user by email: Query error")

    # ------------------------------------------------------------------
    # Tests for read_email_by_id
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_read_email_by_id_success(self, mock_get_db_connection):
        """Test retrieving email by user ID."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {'email': 'alice@example.com'}
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        email = read_email_by_id('some-uuid-123')
        self.assertEqual(email, 'alice@example.com')

        mock_get_db_connection.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "SELECT email FROM users WHERE id = %s;", 
            ('some-uuid-123',)
        )
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_read_email_by_id_no_user(self, mock_get_db_connection):
        """Test returning None if no user found by ID when reading email."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        email = read_email_by_id('nonexistent-uuid')
        self.assertIsNone(email)

        mock_get_db_connection.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_read_email_by_id_exception(self, mock_get_db_connection, mock_log_error):
        """Test exception when reading email by ID."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Query error')
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        email = read_email_by_id('some-uuid-123')
        self.assertIsNone(email)

        mock_get_db_connection.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

        mock_log_error.assert_called_once_with("Error retrieving user email by ID: Query error")

    # ------------------------------------------------------------------
    # Tests for update_user_display_name
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_update_user_display_name_success(self, mock_get_db_connection):
        """Test updating user's display name by email, success scenario."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = update_user_display_name('NewName', 'alice@example.com')
        self.assertTrue(result)

        mock_get_db_connection.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "UPDATE users SET display_name = %s WHERE email = %s;",
            ('NewName', 'alice@example.com')
        )
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_update_user_display_name_db_connection_failure(self, mock_get_db_connection, mock_log_error):
        """Test DB connection failure for update_user_display_name."""
        mock_get_db_connection.return_value = None

    
        result = update_user_display_name('AnotherName', 'bob@example.com')
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()
        mock_log_error.assert_called_once_with("Failed to connect to the database.")

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_update_user_display_name_exception(self, mock_get_db_connection, mock_log_error):
        """Test exception scenario for update_user_display_name."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Update error')
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = update_user_display_name('AnotherName', 'bob@example.com')
        self.assertFalse(result)

        mock_get_db_connection.assert_called_once()
        mock_conn.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

        mock_log_error.assert_called_once_with("Error updating user display name: Update error")

    # ------------------------------------------------------------------
    # Tests for delete_user
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_delete_user_success(self, mock_get_db_connection):
        """Test successful delete of user by ID."""
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

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_delete_user_db_connection_failure(self, mock_get_db_connection, mock_log_error):
        """Test DB connection failure scenario for delete_user."""
        mock_get_db_connection.return_value = None

        result = delete_user('some-uuid-123')
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()
        mock_log_error.assert_called_once_with("Failed to connect to the database.")

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_delete_user_exception(self, mock_get_db_connection, mock_log_error):
        """Test exception scenario for delete_user."""
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

        mock_log_error.assert_called_once_with("Error deleting user: Delete error")


if __name__ == '__main__':
    unittest.main()