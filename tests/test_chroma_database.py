# test_chroma_database.py

import unittest
from unittest.mock import patch, MagicMock
import chromadb

# Import the functions to test
from backend.database.chroma_database import (
    generate_embedding,
    initialize_chromadb,
    get_or_create_collection,
    add_documents,
    retrieve_by_file_name,
    update_entry,
    delete_entry,
    nearest_neighbor_search
)

class TestChromaDatabase(unittest.TestCase):

    def setUp(self):
        # Initialize client and collection
        self.client = initialize_chromadb()
        self.collection_name = 'test_collection'
        self.collection = get_or_create_collection(self.client, self.collection_name)
        # Retrieve all document IDs
        all_documents = self.collection.get()
        all_ids = all_documents.get('ids', [])
        # Delete all documents by IDs if any exist
        if all_ids:
            self.collection.delete(ids=all_ids)

    @unittest.skip("Skipping due to ChromaDB singleton limitation")
    def test_initialize_chromadb_with_persistence(self):
        # This test is skipped because ChromaDB cannot be re-initialized with different settings
        pass

    # def test_initialize_chromadb_with_persistence(self):
    #     # Arrange
    #     persist_directory = 'test_persist_directory'

    #     # Act
    #     client = initialize_chromadb(use_persistence=True, persist_directory=persist_directory)

    #     # Assert
    #     self.assertIsInstance(client, chromadb.Client)

    @patch('backend.database.chroma_database.openai.embeddings.create')
    def test_generate_embedding(self, mock_create):
        # Arrange
        mock_response = {
            'data': [{'embedding': [0.1, 0.2, 0.3]}]
        }
        mock_create.return_value = mock_response
        text = "Test text"

        # Act
        embedding = generate_embedding(text)

        # Assert
        mock_create.assert_called_once_with(
            input=text,
            model='text-embedding-ada-002'
        )
        self.assertEqual(embedding, [0.1, 0.2, 0.3])

    def test_initialize_chromadb_without_persistence(self):
        # Act
        client = initialize_chromadb()

        # Assert
        self.assertIsNotNone(client)
        self.assertTrue(hasattr(client, 'get_or_create_collection'))



    def test_get_or_create_collection(self):
        # Arrange
        client = initialize_chromadb()
        collection_name = 'test_collection'

        # Act
        collection = get_or_create_collection(client, collection_name)

        # Assert
        self.assertEqual(collection.name, collection_name)

    @patch('backend.database.chroma_database.generate_embedding')
    def test_add_documents(self, mock_generate_embedding):
        # Arrange
        mock_generate_embedding.return_value = [0.1, 0.2, 0.3]
        client = initialize_chromadb()
        collection = get_or_create_collection(client, 'test_collection')

        documents = ["Document 1", "Document 2"]
        ids = ["doc1", "doc2"]
        metadatas = [{"file_name": "file1.txt"}, {"file_name": "file2.txt"}]

        # Act
        add_documents(collection, documents, ids, metadatas)

        # Assert
        result = collection.get()
        self.assertEqual(len(result['documents']), 2)
        mock_generate_embedding.assert_any_call("Document 1")
        mock_generate_embedding.assert_any_call("Document 2")

    @patch('backend.database.chroma_database.generate_embedding')
    def test_retrieve_by_file_name(self, mock_generate_embedding):
        # Arrange
        mock_generate_embedding.return_value = [0.1, 0.2, 0.3]
        client = initialize_chromadb()
        collection = get_or_create_collection(client, 'test_collection')
        documents = ["Document 1", "Document 2"]
        ids = ["doc1", "doc2"]
        metadatas = [{"file_name": "file1.txt"}, {"file_name": "file2.txt"}]
        add_documents(collection, documents, ids, metadatas)

        # Act
        results = retrieve_by_file_name(collection, 'file1.txt')

        # Assert
        self.assertEqual(len(results['documents']), 1)
        self.assertEqual(results['metadatas'][0]['file_name'], 'file1.txt')

    @patch('backend.database.chroma_database.generate_embedding')
    def test_update_entry(self, mock_generate_embedding):
        # Arrange
        mock_generate_embedding.return_value = [0.4, 0.5, 0.6]
        client = initialize_chromadb()
        collection = get_or_create_collection(client, 'test_collection')
        documents = ["Original Document"]
        ids = ["doc1"]
        metadatas = [{"file_name": "file1.txt"}]
        add_documents(collection, documents, ids, metadatas)

        updated_document = "Updated Document"
        updated_metadata = {"file_name": "updated_file1.txt"}

        # Reset the mock to clear previous calls
        mock_generate_embedding.reset_mock()

        # Act
        update_entry(collection, "doc1", updated_document=updated_document, updated_metadata=updated_metadata)

        # Assert
        result = collection.get(ids=["doc1"])
        self.assertEqual(result['documents'][0], updated_document)
        self.assertEqual(result['metadatas'][0]['file_name'], "updated_file1.txt")
        mock_generate_embedding.assert_called_once_with(updated_document)

    @patch('backend.database.chroma_database.generate_embedding')
    def test_delete_entry(self, mock_generate_embedding):
        # Arrange
        mock_generate_embedding.return_value = [0.1, 0.2, 0.3]
        client = initialize_chromadb()
        collection = get_or_create_collection(client, 'test_collection')
        documents = ["Document to delete"]
        ids = ["doc1"]
        metadatas = [{"file_name": "file1.txt"}]
        add_documents(collection, documents, ids, metadatas)

        # Act
        delete_entry(collection, "doc1")

        # Assert
        result = collection.get(ids=["doc1"])
        self.assertEqual(len(result['documents']), 0)

    @patch('backend.database.chroma_database.generate_embedding')
    def test_nearest_neighbor_search(self, mock_generate_embedding):
        # Arrange
        embeddings = {
            "Document 1": [0.1, 0.2, 0.3],
            "Document 2": [0.4, 0.5, 0.6]
        }

        def side_effect(text):
            return embeddings.get(text, [0.0, 0.0, 0.0])

        mock_generate_embedding.side_effect = side_effect

        client = initialize_chromadb()
        collection = get_or_create_collection(client, 'test_collection')

        documents = ["Document 1", "Document 2"]
        ids = ["doc1", "doc2"]
        metadatas = [{"file_name": "file1.txt"}, {"file_name": "file2.txt"}]
        add_documents(collection, documents, ids, metadatas)

        input_text = "Document 1"

        # Act
        results = nearest_neighbor_search(collection, input_text, n_results=2)

        # Assert
        self.assertEqual(len(results['documents'][0]), 2)
        self.assertIn("Document 1", results['documents'][0])
        self.assertIn("Document 2", results['documents'][0])
        mock_generate_embedding.assert_called_with(input_text)

if __name__ == '__main__':
    unittest.main()