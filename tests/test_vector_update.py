import unittest
from unittest.mock import patch, MagicMock

# Import the functions under test
from backend.database.vectorUpdate import update_embedding_by_id, update_embedding_by_title

class TestUpdateEmbedding(unittest.TestCase):

    @patch('vectorUpdate.get_embeddings')
    @patch('vectorUpdate.get_db_connection')
    def test_update_embedding_by_id_success(self, mock_get_db_connection, mock_get_embeddings):
        # Mock the embedding generation
        mock_embedding = [0.1] * 1536  # Mock embedding of correct size
        mock_get_embeddings.return_value = [{'embedding': mock_embedding, 'text': 'Updated content.'}]

        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Configure cursor.rowcount to simulate a successful update
        mock_cursor.rowcount = 1

        # Call the function under test
        record_id = 1
        new_content = "Updated content."
        result = update_embedding_by_id(record_id, new_content)

        # Assertions
        self.assertTrue(result)
        mock_get_embeddings.assert_called_once_with([new_content])
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch('vectorUpdate.get_embeddings')
    @patch('vectorUpdate.get_db_connection')
    def test_update_embedding_by_id_no_record_found(self, mock_get_db_connection, mock_get_embeddings):
        # Mock the embedding generation
        mock_embedding = [0.1] * 1536
        mock_get_embeddings.return_value = [{'embedding': mock_embedding, 'text': 'Updated content.'}]

        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Configure cursor.rowcount to simulate no records updated
        mock_cursor.rowcount = 0

        # Call the function under test
        record_id = 9999  # Assuming this ID does not exist
        new_content = "Updated content."
        result = update_embedding_by_id(record_id, new_content)

        # Assertions
        self.assertFalse(result)
        mock_get_embeddings.assert_called_once_with([new_content])
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch('vectorUpdate.get_embeddings')
    @patch('vectorUpdate.get_db_connection')
    def test_update_embedding_by_id_db_connection_failure(self, mock_get_db_connection, mock_get_embeddings):
        # Mock the embedding generation
        mock_embedding = [0.1] * 1536
        mock_get_embeddings.return_value = [{'embedding': mock_embedding, 'text': 'Updated content.'}]

        # Mock get_db_connection to return None
        mock_get_db_connection.return_value = None

        # Call the function under test
        record_id = 1
        new_content = "Updated content."
        result = update_embedding_by_id(record_id, new_content)

        # Assertions
        self.assertFalse(result)
        mock_get_embeddings.assert_called_once_with([new_content])

    @patch('vectorUpdate.get_embeddings')
    @patch('vectorUpdate.get_db_connection')
    def test_update_embedding_by_id_exception(self, mock_get_db_connection, mock_get_embeddings):
        # Mock the embedding generation
        mock_embedding = [0.1] * 1536
        mock_get_embeddings.return_value = [{'embedding': mock_embedding, 'text': 'Updated content.'}]

        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Configure cursor.execute to raise an exception
        mock_cursor.execute.side_effect = Exception('Database error')

        # Call the function under test
        record_id = 1
        new_content = "Updated content."
        result = update_embedding_by_id(record_id, new_content)

        # Assertions
        self.assertFalse(result)
        mock_conn.rollback.assert_called_once()
        mock_conn.close.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch('vectorUpdate.get_embeddings')
    @patch('vectorUpdate.get_db_connection')
    def test_update_embedding_by_title_success(self, mock_get_db_connection, mock_get_embeddings):
        # Mock the embedding generation
        mock_embedding = [0.1] * 1536
        mock_get_embeddings.return_value = [{'embedding': mock_embedding, 'text': 'Updated content.'}]

        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Configure cursor.rowcount to simulate a successful update
        mock_cursor.rowcount = 1

        # Call the function under test
        title = "Existing Title"
        new_content = "Updated content."
        result = update_embedding_by_title(title, new_content)

        # Assertions
        self.assertTrue(result)
        mock_get_embeddings.assert_called_once_with([new_content])
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch('vectorUpdate.get_embeddings')
    @patch('vectorUpdate.get_db_connection')
    def test_update_embedding_by_title_no_record_found(self, mock_get_db_connection, mock_get_embeddings):
        # Mock the embedding generation
        mock_embedding = [0.1] * 1536
        mock_get_embeddings.return_value = [{'embedding': mock_embedding, 'text': 'Updated content.'}]

        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Configure cursor.rowcount to simulate no records updated
        mock_cursor.rowcount = 0

        # Call the function under test
        title = "Nonexistent Title"
        new_content = "Updated content."
        result = update_embedding_by_title(title, new_content)

        # Assertions
        self.assertFalse(result)
        mock_get_embeddings.assert_called_once_with([new_content])
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch('vectorUpdate.get_embeddings')
    @patch('vectorUpdate.get_db_connection')
    def test_update_embedding_by_title_db_connection_failure(self, mock_get_db_connection, mock_get_embeddings):
        # Mock the embedding generation
        mock_embedding = [0.1] * 1536
        mock_get_embeddings.return_value = [{'embedding': mock_embedding, 'text': 'Updated content.'}]

        # Mock get_db_connection to return None
        mock_get_db_connection.return_value = None

        # Call the function under test
        title = "Existing Title"
        new_content = "Updated content."
        result = update_embedding_by_title(title, new_content)

        # Assertions
        self.assertFalse(result)
        mock_get_embeddings.assert_called_once_with([new_content])

    @patch('vectorUpdate.get_embeddings')
    @patch('vectorUpdate.get_db_connection')
    def test_update_embedding_by_title_exception(self, mock_get_db_connection, mock_get_embeddings):
        # Mock the embedding generation
        mock_embedding = [0.1] * 1536
        mock_get_embeddings.return_value = [{'embedding': mock_embedding, 'text': 'Updated content.'}]

        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Configure cursor.execute to raise an exception
        mock_cursor.execute.side_effect = Exception('Database error')

        # Call the function under test
        title = "Existing Title"
        new_content = "Updated content."
        result = update_embedding_by_title(title, new_content)

        # Assertions
        self.assertFalse(result)
        mock_conn.rollback.assert_called_once()
        mock_conn.close.assert_called_once()
        mock_cursor.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()