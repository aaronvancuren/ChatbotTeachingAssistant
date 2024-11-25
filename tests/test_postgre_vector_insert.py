import unittest
from unittest.mock import patch, MagicMock
from psycopg2.extensions import AsIs
import textwrap
import logging

# Import the function under test
from backend.database.postgre_crud_ops import insert_embeddings_into_db

class TestInsertEmbeddingsIntoDb(unittest.TestCase):

    @patch('backend.database.postgre_crud_ops.get_embeddings')
    @patch('backend.database.postgre_crud_ops.get_db_connection')
    @patch('backend.database.postgre_crud_ops.execute_values')
    def test_insert_embeddings_success(self, mock_execute_values, mock_get_db_connection, mock_get_embeddings):
        # Sample input data
        text_chunks = ['Sample text 1', 'Sample text 2', 'Sample text 3']

        # Mock get_embeddings to return embeddings
        mock_get_embeddings.return_value = [
            {'text': 'Sample text 1', 'embedding': [0.1] * 1536},
            {'text': 'Sample text 2', 'embedding': [0.2] * 1536},
            {'text': 'Sample text 3', 'embedding': [0.3] * 1536},
        ]

        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Mock cursor.fetchall to return inserted IDs
        mock_cursor.fetchall.return_value = [(1,), (2,), (3,)]

        # Call the function under test
        result = insert_embeddings_into_db(text_chunks)

        # Assertions
        self.assertEqual(result, [1, 2, 3])
        self.assertEqual(mock_get_embeddings.call_count, 1)
        mock_get_embeddings.assert_called_with(text_chunks)

        # Prepare expected records for insertion
        expected_records = []
        for idx, embedding_item in enumerate(mock_get_embeddings.return_value):
            title = f"Insert {idx + 1}"
            content = embedding_item['text']
            embedding = embedding_item['embedding']
            embedding_str = "{" + ",".join(map(str, embedding)) + "}"
            expected_records.append((title, content, AsIs(f"'{embedding_str}'::vector")))

        # Verify that execute_values was called once
        mock_execute_values.assert_called_once()

        # Get the actual call arguments
        actual_args, actual_kwargs = mock_execute_values.call_args

        # Extract the arguments
        actual_cursor = actual_args[0]
        actual_query = actual_args[1]
        actual_records = actual_args[2]
        actual_template = actual_kwargs.get('template')

        # Compare the cursor, query, and template
        self.assertEqual(actual_cursor, mock_cursor)
        insert_query = textwrap.dedent("""
                INSERT INTO course_materials (title, content, embedding)
                VALUES %s
                RETURNING id;
            """)
        self.assertEqual(actual_query, insert_query)
        self.assertEqual(actual_template, "(%s, %s, %s)")

        # Helper function to extract the value from AsIs
        def extract_as_is_value(as_is_obj):
            return as_is_obj.getquoted().decode()

        # Compare each record
        for expected_record, actual_record in zip(expected_records, actual_records):
            self.assertEqual(expected_record[0], actual_record[0])  # title
            self.assertEqual(expected_record[1], actual_record[1])  # content

            # Extract and compare the AsIs values
            expected_embedding = extract_as_is_value(expected_record[2])
            actual_embedding = extract_as_is_value(actual_record[2])
            self.assertEqual(expected_embedding, actual_embedding)

        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgre_crud_ops.get_db_connection')
    @patch('backend.database.postgre_crud_ops.get_embeddings')
    def test_insert_embeddings_empty_input(self, mock_get_embeddings, mock_get_db_connection):
        # Empty input data
        text_chunks = []

        # Call the function under test
        result = insert_embeddings_into_db(text_chunks)

        # Assertions
        self.assertIsNone(result)
        mock_get_embeddings.assert_not_called()
        mock_get_db_connection.assert_not_called()

    @patch('backend.database.postgre_crud_ops.logging')
    @patch('backend.database.postgre_crud_ops.get_db_connection')
    @patch('backend.database.postgre_crud_ops.get_embeddings')
    def test_insert_embeddings_embedding_failure(self, mock_get_embeddings, mock_get_db_connection, mock_logging):
        # Sample input data
        text_chunks = ['Sample text']

        # Mock get_embeddings to return None embedding
        mock_get_embeddings.return_value = [{'text': 'Sample text', 'embedding': None}]

        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Call the function under test
        result = insert_embeddings_into_db(text_chunks)

        # Assertions
        self.assertIsNone(result)
        mock_logging.error.assert_called_with('No embeddings to insert into the database.')
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgre_crud_ops.logging')
    @patch('backend.database.postgre_crud_ops.get_db_connection')
    @patch('backend.database.postgre_crud_ops.get_embeddings')
    def test_insert_embeddings_db_connection_failure(self, mock_get_embeddings, mock_get_db_connection, mock_logging):
        # Sample input data
        text_chunks = ['Sample text']

        # Mock get_embeddings to return embeddings
        mock_get_embeddings.return_value = [{'text': 'Sample text', 'embedding': [0.1] * 1536}]

        # Mock get_db_connection to return None
        mock_get_db_connection.return_value = None

        # Call the function under test
        result = insert_embeddings_into_db(text_chunks)

        # Assertions
        self.assertIsNone(result)
        mock_logging.error.assert_called_with('Failed to connect to the database.')

    @patch('backend.database.postgre_crud_ops.logging')
    @patch('backend.database.postgre_crud_ops.execute_values')
    @patch('backend.database.postgre_crud_ops.get_db_connection')
    @patch('backend.database.postgre_crud_ops.get_embeddings')
    def test_insert_embeddings_db_insertion_error(self, mock_get_embeddings, mock_get_db_connection, mock_execute_values, mock_logging):
        # Sample input data
        text_chunks = ['Sample text']
    
        # Mock get_embeddings to return embeddings
        mock_get_embeddings.return_value = [{'text': 'Sample text', 'embedding': [0.1] * 1536}]
    
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn
    
        # Simulate an exception during insertion
        mock_execute_values.side_effect = Exception('Database insertion error')
    
        # Call the function under test
        result = insert_embeddings_into_db(text_chunks)
    
        # Assertions
        self.assertIsNone(result)
        mock_logging.error.assert_called_with('Database insertion error: Database insertion error')
        mock_conn.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()