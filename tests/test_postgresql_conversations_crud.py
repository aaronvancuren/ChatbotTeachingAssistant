import unittest
from unittest.mock import patch, MagicMock

# Import the updated CRUD methods under test
from backend.database.postgres import (
    create_user_conversation,
    read_conversations_by_user,
    update_conversation_title,
    delete_conversation
)

class TestUserConversationsCrudOps(unittest.TestCase):

    # ------------------------------------------------------------------
    # Tests for create_user_conversation
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_create_user_conversation_success(self, mock_get_db_connection):
        """Test successfully creating a user_conversation."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Mock fetchone to return a newly generated conversation_id (UUID)
        mock_cursor.fetchone.return_value = ['123e4567-e89b-12d3-a456-426614174000']

        # Call the function under test
        conv_id = create_user_conversation(
            course_id='course-uuid-123',
            user_id='user-uuid-456',
            title='My Conversation'
        )

        # Assertions
        self.assertEqual(conv_id, '123e4567-e89b-12d3-a456-426614174000')
        mock_get_db_connection.assert_called_once()

        expected_query = """
            INSERT INTO user_conversations (course_id, user_id, title)
            VALUES (%s, %s, %s)
            RETURNING conversation_id;
        """
        mock_cursor.execute.assert_called_once_with(
            expected_query,
            ('course-uuid-123', 'user-uuid-456', 'My Conversation')
        )
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_create_user_conversation_db_connection_failure(self, mock_get_db_connection, mock_log_error):
        """Test DB connection failure for create_user_conversation."""
        mock_get_db_connection.return_value = None

        conv_id = create_user_conversation('course-uuid-123', 'user-uuid-456', 'Some Title')
        self.assertIsNone(conv_id)

        mock_get_db_connection.assert_called_once()
        mock_log_error.assert_called_once_with("Failed to connect to the database.")

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_create_user_conversation_exception(self, mock_get_db_connection, mock_log_error):
        """Test exception on execute for create_user_conversation."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Insert error')
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        conv_id = create_user_conversation('course-uuid-123', 'user-uuid-456', 'Another Title')
        self.assertIsNone(conv_id)

        mock_get_db_connection.assert_called_once()
        mock_conn.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

        mock_log_error.assert_called_once_with("Error creating user conversation: Insert error")

    # ------------------------------------------------------------------
    # Tests for read_conversations_by_user
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_read_conversations_by_user_success(self, mock_get_db_connection):
        """Test returning conversation IDs for a given user and course."""
        mock_rows = [
            {'conversation_id': 'conv-uuid-111'},
            {'conversation_id': 'conv-uuid-222'}
        ]

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = mock_rows
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = read_conversations_by_user('user-uuid-456', 'course-uuid-999')
        self.assertEqual(result, ['conv-uuid-111', 'conv-uuid-222'])

        mock_get_db_connection.assert_called_once()
        select_query = "SELECT conversation_id FROM user_conversations WHERE user_id = %s AND course_id = %s;"
        mock_cursor.execute.assert_called_once_with(select_query, ('user-uuid-456', 'course-uuid-999'))
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_read_conversations_by_user_no_result(self, mock_get_db_connection):
        """Test returning an empty list when no conversation is found."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = read_conversations_by_user('user-uuid-789', 'course-uuid-999')
        self.assertEqual(result, [])

        mock_get_db_connection.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_read_conversations_by_user_exception(self, mock_get_db_connection, mock_log_error):
        """Test returning an empty list upon exception."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Select error')
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = read_conversations_by_user('user-uuid-456', 'course-uuid-999')
        self.assertEqual(result, [])
        mock_get_db_connection.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

        mock_log_error.assert_called_once_with("Error retrieving conversation ids: Select error")

    # ------------------------------------------------------------------
    # Tests for update_conversation_title
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_update_conversation_title_success(self, mock_get_db_connection):
        """Test updating the conversation title successfully (by conversation_id only)."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = update_conversation_title('conv-uuid-123', 'Updated Title')
        self.assertTrue(result)

        mock_get_db_connection.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "UPDATE user_conversations SET title = %s WHERE conversation_id = %s;",
            ('Updated Title', 'conv-uuid-123')
        )
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_update_conversation_title_db_connection_failure(self, mock_get_db_connection, mock_log_error):
        """Test db connection failure scenario for update_conversation_title."""
        mock_get_db_connection.return_value = None

        result = update_conversation_title('conv-uuid-123', 'New Title')
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()
        mock_log_error.assert_called_once_with("Failed to connect to the database.")

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_update_conversation_title_exception(self, mock_get_db_connection, mock_log_error):
        """Test exception scenario for update_conversation_title."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Update error')
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = update_conversation_title('conv-uuid-234', 'Another Title')
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()
        mock_conn.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

        mock_log_error.assert_called_once_with("Error updating conversation title: Update error")

    # ------------------------------------------------------------------
    # Tests for delete_conversation
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_delete_conversation_success(self, mock_get_db_connection):
        """Test successfully deleting a conversation by conversation_id."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = delete_conversation('conv-uuid-999')
        self.assertTrue(result)

        mock_get_db_connection.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "DELETE FROM user_conversations WHERE conversation_id = %s;", 
            ('conv-uuid-999',)
        )
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_delete_conversation_db_connection_failure(self, mock_get_db_connection, mock_log_error):
        """Test DB connection failure for delete_conversation."""
        mock_get_db_connection.return_value = None

        result = delete_conversation('conv-uuid-999')
        self.assertFalse(result)

        mock_get_db_connection.assert_called_once()
        mock_log_error.assert_called_once_with("Failed to connect to the database.")

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_delete_conversation_exception(self, mock_get_db_connection, mock_log_error):
        """Test exception scenario for delete_conversation."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Delete error')
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = delete_conversation('conv-uuid-999')
        self.assertFalse(result)

        mock_get_db_connection.assert_called_once()
        mock_conn.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

        mock_log_error.assert_called_once_with("Error deleting conversation: Delete error")


if __name__ == '__main__':
    unittest.main()