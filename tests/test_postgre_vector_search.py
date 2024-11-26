import unittest
from unittest.mock import patch, MagicMock
import logging

# Import the function under test
from backend.database.postgre_crud_ops import search_similar_embeddings

class TestSearchSimilarEmbeddings(unittest.TestCase):

    @patch('backend.database.postgre_crud_ops.get_embeddings')
    @patch('backend.database.postgre_crud_ops.get_db_connection')
    def test_search_similar_embeddings_success(self, mock_get_db_connection, mock_get_embeddings):
        # Mock get_embeddings to return a valid embedding
        query_text = 'Test query'
        mock_get_embeddings.return_value = [{'text': query_text, 'embedding': [0.5] * 1536}]

        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Prepare mock results from the database
        mock_results = [
            {'id': 1, 'title': 'Title 1', 'content': 'Content 1'},
            {'id': 2, 'title': 'Title 2', 'content': 'Content 2'}
        ]
        mock_cursor.fetchall.return_value = mock_results

        # Call the function under test
        results = search_similar_embeddings(query_text, top_k=2)

        # Assertions
        self.assertEqual(results, mock_results)
        mock_get_embeddings.assert_called_once_with([query_text])
        mock_get_db_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgre_crud_ops.logging')
    @patch('backend.database.postgre_crud_ops.get_embeddings')
    def test_search_similar_embeddings_embedding_failure(self, mock_get_embeddings, mock_logging):
        # Mock get_embeddings to return None embedding
        query_text = 'Test query'
        mock_get_embeddings.return_value = [{'text': query_text, 'embedding': None}]

        # Call the function under test
        results = search_similar_embeddings(query_text)

        # Assertions
        self.assertEqual(results, [])
        mock_logging.error.assert_called_with("Failed to generate query embedding.")
        mock_get_embeddings.assert_called_once_with([query_text])

    @patch('backend.database.postgre_crud_ops.logging')
    @patch('backend.database.postgre_crud_ops.get_db_connection')
    @patch('backend.database.postgre_crud_ops.get_embeddings')
    def test_search_similar_embeddings_db_connection_failure(self, mock_get_embeddings, mock_get_db_connection, mock_logging):
        # Mock get_embeddings to return a valid embedding
        query_text = 'Test query'
        mock_get_embeddings.return_value = [{'text': query_text, 'embedding': [0.5] * 1536}]

        # Mock get_db_connection to return None
        mock_get_db_connection.return_value = None

        # Call the function under test
        results = search_similar_embeddings(query_text)

        # Assertions
        self.assertEqual(results, [])
        mock_logging.error.assert_called_with("Failed to connect to the database.")
        mock_get_embeddings.assert_called_once_with([query_text])
        mock_get_db_connection.assert_called_once()

    @patch('backend.database.postgre_crud_ops.logging')
    @patch('backend.database.postgre_crud_ops.get_db_connection')
    @patch('backend.database.postgre_crud_ops.get_embeddings')
    def test_search_similar_embeddings_query_exception(self, mock_get_embeddings, mock_get_db_connection, mock_logging):
        # Mock get_embeddings to return a valid embedding
        query_text = 'Test query'
        mock_get_embeddings.return_value = [{'text': query_text, 'embedding': [0.5] * 1536}]

        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Simulate an exception during cursor.execute
        mock_cursor.execute.side_effect = Exception('Database query error')

        # Call the function under test
        results = search_similar_embeddings(query_text)

        # Assertions
        self.assertEqual(results, [])
        mock_logging.error.assert_called_with("Error during similarity search: Database query error")
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()
        mock_get_embeddings.assert_called_once_with([query_text])
        mock_get_db_connection.assert_called_once()

if __name__ == '__main__':
    unittest.main()