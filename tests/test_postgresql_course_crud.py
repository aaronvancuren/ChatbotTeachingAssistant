import unittest
from unittest.mock import patch, MagicMock

# Import the updated functions under test
from backend.database.postgres import (
    create_course,
    read_course_by_id,
    update_course_title,
    update_course_model,
    delete_course
)

class TestCourseCrudOps(unittest.TestCase):

    # ------------------------------------------------------------------
    # Tests for create_course
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_create_course_success(self, mock_get_db_connection):
        """Test creating a course successfully."""
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Simulate returning a new UUID from RETURNING id;
        mock_cursor.fetchone.return_value = ['123e4567-e89b-12d3-a456-426614174000']

        # Call the function under test
        course_id = create_course(
            instructor_id="instructor-uuid-1",
            display_name="Intro to Chemistry",
            subject="CHEM",
            course_number=101,
            section_number=1,
            title="Chemistry Basics",
            model="some_model",
            prompt="Welcome to Chemistry!",
            documents_path="/chem/docs",
            image_path="/chem/image.png"
        )

        # Assertions
        self.assertEqual(course_id, '123e4567-e89b-12d3-a456-426614174000')
        mock_get_db_connection.assert_called_once()

        # Verify the query and parameters
        expected_query = """
            INSERT INTO courses (instructor_id, display_name, subject, course_number, section_number, title, model, prompt, documents_path, image_path)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """
        mock_cursor.execute.assert_called_once_with(
            expected_query,
            (
                "instructor-uuid-1",
                "Intro to Chemistry",
                "CHEM",
                101,
                1,
                "Chemistry Basics",
                "some_model",
                "Welcome to Chemistry!",
                "/chem/docs",
                "/chem/image.png"
            )
        )
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_create_course_db_connection_failure(self, mock_get_db_connection, mock_log_error):
        """Test DB connection failure for create_course."""
        mock_get_db_connection.return_value = None

        # Call the function under test
        course_id = create_course(
            instructor_id="instructor-uuid-2",
            display_name="Intro to Biology",
            subject="BIOL",
            course_number=200,
            section_number=2,
            title="Biology 200",
            model="some_model",
            prompt="Welcome to Biology",
            documents_path="/bio/docs",
            image_path="/bio/image.png"
        )

        # Assertions
        self.assertIsNone(course_id)
        mock_get_db_connection.assert_called_once()
        mock_log_error.assert_called_once_with("Failed to connect to the database.")

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_create_course_exception(self, mock_get_db_connection, mock_log_error):
        """Test exception scenario during course creation."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception('Database error')
        mock_get_db_connection.return_value = mock_conn

        course_id = create_course(
            instructor_id="instructor-uuid-3",
            display_name="Intro to Physics",
            subject="PHYS",
            course_number=300,
            section_number=3,
            title="Physics 300",
            model="another_model",
            prompt="Welcome to Physics!",
            documents_path="/phys/docs",
            image_path="/phys/image.png"
        )

        self.assertIsNone(course_id)
        mock_get_db_connection.assert_called_once()
        mock_conn.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

        mock_log_error.assert_called_once_with("Error creating course: Database error")

    # ------------------------------------------------------------------
    # Tests for read_course_by_id
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_read_course_by_id_success(self, mock_get_db_connection):
        """Test retrieving course by ID successfully."""
        mock_course = {
            'id': '123e4567-e89b-12d3-a456-426614174000',
            'instructor_id': 'instructor-uuid-1',
            'display_name': 'Intro to Chemistry',
            'subject': 'CHEM',
            'course_number': 101,
            'section_number': 1,
            'title': 'Chemistry Basics',
            'model': 'some_model',
            'prompt': 'Welcome to Chemistry!',
            'documents_path': '/chem/docs',
            'image_path': '/chem/image.png',
            'created_at': None,
            'archived': False,
            'archived_by': None,
            'archived_at': None
        }

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = mock_course
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = read_course_by_id('123e4567-e89b-12d3-a456-426614174000')
        self.assertEqual(result, mock_course)

        mock_get_db_connection.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM courses WHERE id = %s;", 
            ('123e4567-e89b-12d3-a456-426614174000',)
        )
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_read_course_by_id_no_course_found(self, mock_get_db_connection):
        """Test returning None when no course is found by ID."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = read_course_by_id('nonexistent-uuid')
        self.assertIsNone(result)

        mock_get_db_connection.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_read_course_by_id_exception(self, mock_get_db_connection, mock_log_error):
        """Test exception scenario for read_course_by_id."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Query error')
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = read_course_by_id('some-uuid')
        self.assertIsNone(result)
        mock_get_db_connection.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

        mock_log_error.assert_called_once_with("Error retrieving course info: Query error")

    # ------------------------------------------------------------------
    # Tests for update_course_title
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_update_course_title_success(self, mock_get_db_connection):
        """Test updating course title successfully."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = update_course_title('123e4567-e89b-12d3-a456-426614174000', 'New Title')
        self.assertTrue(result)

        mock_get_db_connection.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "UPDATE courses SET title = %s WHERE id = %s;",
            ('New Title', '123e4567-e89b-12d3-a456-426614174000')
        )
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_update_course_title_db_connection_failure(self, mock_get_db_connection, mock_log_error):
        """Test db connection failure scenario for update_course_title."""
        mock_get_db_connection.return_value = None

        result = update_course_title('some-uuid', 'Another Title')
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()

        mock_log_error.assert_called_once_with("Failed to connect to the database.")

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_update_course_title_exception(self, mock_get_db_connection, mock_log_error):
        """Test exception scenario for update_course_title."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Update error')
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = update_course_title('some-uuid', 'Another Title')
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()
        mock_conn.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

        mock_log_error.assert_called_once_with("Error updating course title: Update error")

    # ------------------------------------------------------------------
    # Tests for update_course_model
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_update_course_model_success(self, mock_get_db_connection):
        """Test updating course model successfully."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = update_course_model('123e4567-e89b-12d3-a456-426614174000', 'new_model')
        self.assertTrue(result)

        mock_get_db_connection.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "UPDATE courses SET model = %s WHERE id = %s;",
            ('new_model', '123e4567-e89b-12d3-a456-426614174000')
        )
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_update_course_model_db_connection_failure(self, mock_get_db_connection, mock_log_error):
        """Test db connection failure for update_course_model."""
        mock_get_db_connection.return_value = None

        result = update_course_model('some-uuid', 'another_model')
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()
        mock_log_error.assert_called_once_with("Failed to connect to the database.")

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_update_course_model_exception(self, mock_get_db_connection, mock_log_error):
        """Test exception scenario for update_course_model."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Update error')
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = update_course_model('some-uuid', 'another_model')
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()
        mock_conn.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

        mock_log_error.assert_called_once_with("Error updating course model: Update error")

    # ------------------------------------------------------------------
    # Tests for delete_course
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_delete_course_success(self, mock_get_db_connection):
        """Test successfully deleting a course by ID."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = delete_course('123e4567-e89b-12d3-a456-426614174000')
        self.assertTrue(result)

        mock_get_db_connection.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "DELETE FROM courses WHERE id = %s;",
            ('123e4567-e89b-12d3-a456-426614174000',)
        )
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_delete_course_db_connection_failure(self, mock_get_db_connection, mock_log_error):
        """Test db connection failure for delete_course."""
        mock_get_db_connection.return_value = None

        result = delete_course('some-uuid')
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()
        mock_log_error.assert_called_once_with("Failed to connect to the database.")

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_delete_course_exception(self, mock_get_db_connection, mock_log_error):
        """Test exception scenario for delete_course."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Delete error')
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = delete_course('some-uuid')
        self.assertFalse(result)

        mock_get_db_connection.assert_called_once()
        mock_conn.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

        mock_log_error.assert_called_once_with("Error deleting course: Delete error")


if __name__ == '__main__':
    unittest.main()