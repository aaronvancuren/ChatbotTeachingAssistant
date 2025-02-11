import unittest
from unittest.mock import patch, MagicMock
import logging
from psycopg2.extras import RealDictCursor

# Import the CRUD methods under test
from backend.database.postgres import (
    create_message,
    read_messages_from_conversation,
    update_message_conversation_id,
    delete_message
)

class TestMessagesCrudOps(unittest.TestCase):

    # ------------------------------------------------------------------
    # Tests for create_message
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_create_message_success(self, mock_get_db_connection):
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Mock the returned message ID (an integer per your schema)
        mock_cursor.fetchone.return_value = [123]

        # Call the function under test
        message_id = create_message(
            conversation_id='conv-uuid-123',
            prompt='Hello, how are you?',
            response='I am good!'
        )

        # Assertions
        self.assertEqual(message_id, 123)
        mock_get_db_connection.assert_called_once()

        expected_query = """
            INSERT INTO messages (conversation_id, prompt, response)
            VALUES (%s, %s, %s)
            RETURNING id;
        """
        mock_cursor.execute.assert_called_once_with(
            expected_query,
            ('conv-uuid-123', 'Hello, how are you?', 'I am good!')
        )
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_create_message_db_connection_failure(self, mock_get_db_connection):
        mock_get_db_connection.return_value = None

        message_id = create_message('conv-uuid-123', 'Question?', 'Answer!')
        self.assertIsNone(message_id)
        mock_get_db_connection.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_create_message_exception(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Insert error')
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        message_id = create_message('conv-uuid-456', 'Prompt?', 'Response!')
        self.assertIsNone(message_id)
        mock_get_db_connection.assert_called_once()
        mock_conn.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    # ------------------------------------------------------------------
    # Tests for read_messages_from_conversation
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_read_messages_from_conversation_success(self, mock_get_db_connection):
        # Each row is a dict with 'prompt' and 'response'
        mock_rows = [
            {'prompt': 'Hello', 'response': 'Hi there!'},
            {'prompt': 'How are you?', 'response': 'Doing well!'}
        ]

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = mock_rows
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        messages = read_messages_from_conversation('conv-uuid-123')
        self.assertEqual(messages, mock_rows)

        mock_get_db_connection.assert_called_once()
        query = """
            SELECT prompt, response FROM messages WHERE conversation_id = %s ORDER BY id ASC;
        """
        mock_cursor.execute.assert_called_once_with(query, ('conv-uuid-123',))
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_read_messages_from_conversation_no_result(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []  # No messages
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        messages = read_messages_from_conversation('conv-uuid-789')
        self.assertEqual(messages, [])
        mock_get_db_connection.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_read_messages_from_conversation_exception(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Select error')
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        messages = read_messages_from_conversation('conv-uuid-123')
        self.assertEqual(messages, [])
        mock_get_db_connection.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    # ------------------------------------------------------------------
    # Tests for update_message_conversation_id
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_update_message_conversation_id_success(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = update_message_conversation_id(
            old_conversation_id='old-conv-uuid',
            new_conversation_id='new-conv-uuid'
        )
        self.assertTrue(result)
        mock_get_db_connection.assert_called_once()

        query = "UPDATE messages SET conversation_id = %s WHERE conversation_id = %s;"
        mock_cursor.execute.assert_called_once_with(query, ('new-conv-uuid', 'old-conv-uuid'))
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_update_message_conversation_id_db_connection_failure(self, mock_get_db_connection):
        mock_get_db_connection.return_value = None
        result = update_message_conversation_id('old-conv-uuid', 'new-conv-uuid')
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_update_message_conversation_id_exception(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Update error')
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = update_message_conversation_id('old-conv-uuid', 'new-conv-uuid')
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()
        mock_conn.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    # ------------------------------------------------------------------
    # Tests for delete_message
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_delete_message_success(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = delete_message('123')  # Per schema, message id is integer, but we pass str -> DB can cast
        self.assertTrue(result)
        mock_get_db_connection.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "DELETE FROM messages WHERE id = %s;",
            ('123',)
        )
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_delete_message_db_connection_failure(self, mock_get_db_connection):
        mock_get_db_connection.return_value = None
        result = delete_message('456')
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_delete_message_exception(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Delete error')
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = delete_message('789')
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()
        mock_conn.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()