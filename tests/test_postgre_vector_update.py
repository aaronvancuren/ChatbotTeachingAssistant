import unittest
from unittest.mock import patch, MagicMock
import logging
import textwrap
from psycopg2.extensions import AsIs

# Import the functions under test
from backend.database.postgre_crud_ops import update_embedding_by_id, update_embedding_by_title

class TestUpdateEmbedding(unittest.TestCase):

    # Tests for update_embedding_by_id
    @patch('backend.database.postgre_crud_ops.get_embeddings')
    @patch('backend.database.postgre_crud_ops.get_db_connection')
    def test_update_embedding_by_id_success(self, mock_get_db_connection, mock_get_embeddings):
        # Mock get_embeddings to return a valid embedding
        new_content = 'Updated content'
        mock_get_embeddings.return_value = [{'text': new_content, 'embedding': [0.5] * 1536}]

        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Configure cursor.rowcount to simulate a successful update
        mock_cursor.rowcount = 1

        # Call the function under test
        record_id = 1
        result = update_embedding_by_id(record_id, new_content)

        # Assertions
        self.assertTrue(result)
        mock_get_embeddings.assert_called_once_with([new_content])
        mock_get_db_connection.assert_called_once()
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgre_crud_ops.logging')
    @patch('backend.database.postgre_crud_ops.get_embeddings')
    def test_update_embedding_by_id_embedding_failure(self, mock_get_embeddings, mock_logging):
        # Mock get_embeddings to return None embedding
        new_content = 'Updated content'
        mock_get_embeddings.return_value = [{'text': new_content, 'embedding': None}]

        # Call the function under test
        record_id = 1
        result = update_embedding_by_id(record_id, new_content)

        # Assertions
        self.assertFalse(result)
        mock_logging.error.assert_called_with("Failed to generate new embedding.")
        mock_get_embeddings.assert_called_once_with([new_content])

    @patch('backend.database.postgre_crud_ops.logging')
    @patch('backend.database.postgre_crud_ops.get_db_connection')
    @patch('backend.database.postgre_crud_ops.get_embeddings')
    def test_update_embedding_by_id_db_connection_failure(self, mock_get_embeddings, mock_get_db_connection, mock_logging):
        # Mock get_embeddings to return a valid embedding
        new_content = 'Updated content'
        mock_get_embeddings.return_value = [{'text': new_content, 'embedding': [0.5] * 1536}]

        # Mock get_db_connection to return None
        mock_get_db_connection.return_value = None

        # Call the function under test
        record_id = 1
        result = update_embedding_by_id(record_id, new_content)

        # Assertions
        self.assertFalse(result)
        mock_logging.error.assert_called_with("Failed to connect to the database.")
        mock_get_embeddings.assert_called_once_with([new_content])
        mock_get_db_connection.assert_called_once()

    @patch('backend.database.postgre_crud_ops.logging')
    @patch('backend.database.postgre_crud_ops.get_db_connection')
    @patch('backend.database.postgre_crud_ops.get_embeddings')
    def test_update_embedding_by_id_no_record_found(self, mock_get_embeddings, mock_get_db_connection, mock_logging):
        # Mock get_embeddings to return a valid embedding
        new_content = 'Updated content'
        mock_get_embeddings.return_value = [{'text': new_content, 'embedding': [0.5] * 1536}]

        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0  # Simulate no record found
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Call the function under test
        record_id = 9999  # Assuming this ID does not exist
        result = update_embedding_by_id(record_id, new_content)

        # Assertions
        self.assertFalse(result)
        mock_logging.warning.assert_called_with(f"No record found with id: {record_id}")
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()
        mock_get_embeddings.assert_called_once_with([new_content])
        mock_get_db_connection.assert_called_once()

    @patch('backend.database.postgre_crud_ops.logging')
    @patch('backend.database.postgre_crud_ops.get_db_connection')
    @patch('backend.database.postgre_crud_ops.get_embeddings')
    def test_update_embedding_by_id_exception(self, mock_get_embeddings, mock_get_db_connection, mock_logging):
        # Mock get_embeddings to return a valid embedding
        new_content = 'Updated content'
        mock_get_embeddings.return_value = [{'text': new_content, 'embedding': [0.5] * 1536}]

        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Database update error')
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Call the function under test
        record_id = 1
        result = update_embedding_by_id(record_id, new_content)

        # Assertions
        self.assertFalse(result)
        mock_logging.error.assert_called_with(f"Error updating record with id '{record_id}': Database update error")
        mock_conn.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()
        mock_get_embeddings.assert_called_once_with([new_content])
        mock_get_db_connection.assert_called_once()

    # Tests for update_embedding_by_title
    @patch('backend.database.postgre_crud_ops.get_embeddings')
    @patch('backend.database.postgre_crud_ops.get_db_connection')
    def test_update_embedding_by_title_success(self, mock_get_db_connection, mock_get_embeddings):
        # Mock get_embeddings to return a valid embedding
        new_content = 'Updated content'
        mock_get_embeddings.return_value = [{'text': new_content, 'embedding': [0.5] * 1536}]

        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Configure cursor.rowcount to simulate a successful update
        mock_cursor.rowcount = 1

        # Call the function under test
        title = 'Existing Title'
        result = update_embedding_by_title(title, new_content)

        # Assertions
        self.assertTrue(result)
        mock_get_embeddings.assert_called_once_with([new_content])
        mock_get_db_connection.assert_called_once()
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgre_crud_ops.logging')
    @patch('backend.database.postgre_crud_ops.get_embeddings')
    def test_update_embedding_by_title_embedding_failure(self, mock_get_embeddings, mock_logging):
        # Mock get_embeddings to return None embedding
        new_content = 'Updated content'
        mock_get_embeddings.return_value = [{'text': new_content, 'embedding': None}]

        # Call the function under test
        title = 'Existing Title'
        result = update_embedding_by_title(title, new_content)

        # Assertions
        self.assertFalse(result)
        mock_logging.error.assert_called_with("Failed to generate new embedding.")
        mock_get_embeddings.assert_called_once_with([new_content])

    @patch('backend.database.postgre_crud_ops.logging')
    @patch('backend.database.postgre_crud_ops.get_db_connection')
    @patch('backend.database.postgre_crud_ops.get_embeddings')
    def test_update_embedding_by_title_db_connection_failure(self, mock_get_embeddings, mock_get_db_connection, mock_logging):
        # Mock get_embeddings to return a valid embedding
        new_content = 'Updated content'
        mock_get_embeddings.return_value = [{'text': new_content, 'embedding': [0.5] * 1536}]

        # Mock get_db_connection to return None
        mock_get_db_connection.return_value = None

        # Call the function under test
        title = 'Existing Title'
        result = update_embedding_by_title(title, new_content)

        # Assertions
        self.assertFalse(result)
        mock_logging.error.assert_called_with("Failed to connect to the database.")
        mock_get_embeddings.assert_called_once_with([new_content])
        mock_get_db_connection.assert_called_once()

    @patch('backend.database.postgre_crud_ops.logging')
    @patch('backend.database.postgre_crud_ops.get_db_connection')
    @patch('backend.database.postgre_crud_ops.get_embeddings')
    def test_update_embedding_by_title_no_record_found(self, mock_get_embeddings, mock_get_db_connection, mock_logging):
        # Mock get_embeddings to return a valid embedding
        new_content = 'Updated content'
        mock_get_embeddings.return_value = [{'text': new_content, 'embedding': [0.5] * 1536}]

        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0  # Simulate no record found
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Call the function under test
        title = 'Nonexistent Title'
        result = update_embedding_by_title(title, new_content)

        # Assertions
        self.assertFalse(result)
        mock_logging.warning.assert_called_with(f"No record found with title: {title}")
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()
        mock_get_embeddings.assert_called_once_with([new_content])
        mock_get_db_connection.assert_called_once()

    @patch('backend.database.postgre_crud_ops.logging')
    @patch('backend.database.postgre_crud_ops.get_db_connection')
    @patch('backend.database.postgre_crud_ops.get_embeddings')
    def test_update_embedding_by_title_exception(self, mock_get_embeddings, mock_get_db_connection, mock_logging):
        # Mock get_embeddings to return a valid embedding
        new_content = 'Updated content'
        mock_get_embeddings.return_value = [{'text': new_content, 'embedding': [0.5] * 1536}]

        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Database update error')
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Call the function under test
        title = 'Existing Title'
        result = update_embedding_by_title(title, new_content)

        # Assertions
        self.assertFalse(result)
        mock_logging.error.assert_called_with(f"Error updating record with title '{title}': Database update error")
        mock_conn.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()
        mock_get_embeddings.assert_called_once_with([new_content])
        mock_get_db_connection.assert_called_once()

if __name__ == '__main__':
    unittest.main