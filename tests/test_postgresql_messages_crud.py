import unittest
from unittest.mock import patch, MagicMock

# Import only the two updated CRUD methods
from backend.database.postgres import (
    create_message,
    read_messages_from_conversation
)

class TestMessagesCrudOps(unittest.TestCase):

    # ------------------------------------------------------------------
    # Tests for create_message
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_create_message_success(self, mock_get_db_connection):
        """Test successfully creating a message."""
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Mock the returned message ID (an integer per the schema)
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

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_create_message_db_connection_failure(self, mock_get_db_connection, mock_log_error):
        """Test DB connection failure scenario for create_message."""
        mock_get_db_connection.return_value = None

        message_id = create_message('conv-uuid-123', 'Question?', 'Answer!')
        self.assertIsNone(message_id)
        mock_get_db_connection.assert_called_once()

        mock_log_error.assert_called_once_with("Failed to connect to the database.")

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_create_message_exception(self, mock_get_db_connection, mock_log_error):
        """Test exception scenario during INSERT query for create_message."""
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

        mock_log_error.assert_called_once_with("Error adding message: Insert error")

    # ------------------------------------------------------------------
    # Tests for read_messages_from_conversation
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_read_messages_from_conversation_success(self, mock_get_db_connection):
        """Test retrieving messages (prompt/response) for a conversation."""
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
        """Test returning an empty list when no messages are found."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        messages = read_messages_from_conversation('conv-uuid-789')
        self.assertEqual(messages, [])
        mock_get_db_connection.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_read_messages_from_conversation_exception(self, mock_get_db_connection, mock_log_error):
        """Test returning an empty list upon exception."""
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

        mock_log_error.assert_called_once_with("Error retrieving messages: Select error")


if __name__ == '__main__':
    unittest.main()