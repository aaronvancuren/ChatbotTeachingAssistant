# made with ChatGPT

import unittest
from unittest.mock import patch, MagicMock
import os
import shutil
import tempfile

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
        # Create a temporary directory for persistent storage
        self.test_persistence_path = tempfile.mkdtemp()

        # Set the environment variable to the temporary directory
        os.environ["CHROMA_PERSISTENT_DIRECTORY"] = self.test_persistence_path

        # Initialize client and collection
        self.client = initialize_chromadb(use_persistence=True)
        self.collection_name = 'test_collection'
        self.collection = get_or_create_collection(self.client, self.collection_name)

        # Retrieve all document IDs
        all_documents = self.collection.get()
        all_ids = all_documents.get('ids', [])
        # Delete all documents by IDs if any exist
        if all_ids:
            self.collection.delete(ids=all_ids)

    def tearDown(self):
        # Clean up after tests
        if hasattr(self, 'client'):
            del self.client
        if os.path.exists(self.test_persistence_path):
            shutil.rmtree(self.test_persistence_path)
        if "CHROMA_PERSISTENT_DIRECTORY" in os.environ:
            del os.environ["CHROMA_PERSISTENT_DIRECTORY"]

    @patch('backend.database.chroma_database.openai.embeddings.create')
    def test_generate_embedding(self, mock_create):
        # Arrange
        # Create a mock response object with 'data' attribute
        mock_data = MagicMock()
        mock_embedding = MagicMock()
        mock_embedding.embedding = [0.1, 0.2, 0.3]
        mock_data.__getitem__.return_value = mock_embedding  # For data[0]
        
        mock_response = MagicMock()
        mock_response.data = [mock_embedding]
        
        mock_create.return_value = mock_response
        text = "Test text"

        # Act
        embedding = generate_embedding(text)

        # Assert
        mock_create.assert_called_once_with(
            input=text,
            model=os.getenv("OPENAI_EMBEDDING_MODEL")
        )
        self.assertEqual(embedding, [0.1, 0.2, 0.3])

    def test_initialize_chromadb_without_persistence(self):
        # Act
        client = initialize_chromadb()

        # Assert
        self.assertIsNotNone(client)
        self.assertTrue(hasattr(client, 'get_or_create_collection'))

    @patch('backend.database.chroma_database.generate_embedding')
    def test_persistent_client(self, mock_generate_embedding):
        # Arrange
        # Set up a test path for persistent storage
        test_persistence_path = 'test_chroma_db'
        os.environ["CHROMA_PERSISTANT_DIRECTORY"] = test_persistence_path

        # Ensure the persistence directory is clean before the test
        if os.path.exists(test_persistence_path):
            import shutil
            shutil.rmtree(test_persistence_path)

        # Mock the embedding generation
        mock_generate_embedding.return_value = [0.1, 0.2, 0.3]

        # Initialize the persistent client and collection
        client = initialize_chromadb(use_persistence=True)
        collection_name = 'test_persistent_collection'
        collection = get_or_create_collection(client, collection_name)

        # Add documents to the collection
        documents = ["Persistent Document 1", "Persistent Document 2"]
        ids = ["pdoc1", "pdoc2"]
        metadatas = [{"file_name": "pfile1.txt"}, {"file_name": "pfile2.txt"}]
        add_documents(collection, documents, ids, metadatas)

        # Close the client to simulate ending the session
        del client

        # Re-initialize the client and collection
        client = initialize_chromadb(use_persistence=True)
        collection = get_or_create_collection(client, collection_name)

        # Act
        # Retrieve documents from the collection
        result = collection.get()

        # Assert
        self.assertEqual(len(result['documents']), 2)
        self.assertIn("Persistent Document 1", result['documents'])
        self.assertIn("Persistent Document 2", result['documents'])

        # Clean up
        collection.delete(ids=ids)
        del client

        # Remove the test persistence directory after the test
        if os.path.exists(test_persistence_path):
            import shutil
            shutil.rmtree(test_persistence_path)

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
        self.assertEqual(len(results), 2)
        self.assertIn("Document 1", [doc['content'] for doc in results])
        self.assertIn("Document 2", [doc['content'] for doc in results])
        mock_generate_embedding.assert_called_with(input_text)

if __name__ == '__main__':
    unittest.main()