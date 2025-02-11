import unittest
from unittest.mock import patch, MagicMock
import logging
from psycopg2.extras import RealDictCursor

# Import the functions under test
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
        # Mock the database connection and cursor
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

    @patch('backend.database.postgres.get_db_connection')
    def test_create_user_conversation_db_connection_failure(self, mock_get_db_connection):
        # Mock get_db_connection to return None
        mock_get_db_connection.return_value = None

        conv_id = create_user_conversation(
            'course-uuid-123', 'user-uuid-456', 'Some Title'
        )
        self.assertIsNone(conv_id)
        mock_get_db_connection.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_create_user_conversation_exception(self, mock_get_db_connection):
        # Mock an exception on execute
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Insert error')
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        conv_id = create_user_conversation(
            'course-uuid-123', 'user-uuid-456', 'Another Title'
        )
        self.assertIsNone(conv_id)
        mock_get_db_connection.assert_called_once()
        mock_conn.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    # ------------------------------------------------------------------
    # Tests for read_conversations_by_user
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_read_conversations_by_user_success(self, mock_get_db_connection):
        # Mock data: each row is a dict with 'conversation_id'
        mock_rows = [
            {'conversation_id': 'conv-uuid-111'},
            {'conversation_id': 'conv-uuid-222'}
        ]

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = mock_rows
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = read_conversations_by_user('user-uuid-456')
        self.assertEqual(result, ['conv-uuid-111', 'conv-uuid-222'])

        mock_get_db_connection.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "SELECT conversation_id FROM user_conversations WHERE user_id = %s;", 
            ('user-uuid-456',)
        )
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_read_conversations_by_user_no_result(self, mock_get_db_connection):
        # Mock empty fetch
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = read_conversations_by_user('user-uuid-789')
        self.assertEqual(result, [])
        mock_get_db_connection.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_read_conversations_by_user_exception(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Select error')
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = read_conversations_by_user('user-uuid-456')
        self.assertEqual(result, [])
        mock_get_db_connection.assert_called_once()
        mock_conn.close.assert_called_once()
        mock_cursor.close.assert_called_once()

    # ------------------------------------------------------------------
    # Tests for update_conversation_title
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_update_conversation_title_success(self, mock_get_db_connection):
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = update_conversation_title(
            conversation_id='conv-uuid-123',
            course_id='course-uuid-456',
            new_title='Updated Title'
        )

        self.assertTrue(result)
        mock_get_db_connection.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "UPDATE user_conversations SET title = %s WHERE conversation_id = %s AND course_id = %s;",
            ('Updated Title', 'conv-uuid-123', 'course-uuid-456')
        )
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_update_conversation_title_db_connection_failure(self, mock_get_db_connection):
        mock_get_db_connection.return_value = None

        result = update_conversation_title('conv-uuid-123', 'course-uuid-456', 'New Title')
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_update_conversation_title_exception(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Update error')
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = update_conversation_title('conv-uuid-234', 'course-uuid-456', 'Another Title')
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()
        mock_conn.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    # ------------------------------------------------------------------
    # Tests for delete_conversation
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_delete_conversation_success(self, mock_get_db_connection):
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

    @patch('backend.database.postgres.get_db_connection')
    def test_delete_conversation_db_connection_failure(self, mock_get_db_connection):
        mock_get_db_connection.return_value = None

        result = delete_conversation('conv-uuid-999')
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_delete_conversation_exception(self, mock_get_db_connection):
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

if __name__ == '__main__':
    unittest.main()