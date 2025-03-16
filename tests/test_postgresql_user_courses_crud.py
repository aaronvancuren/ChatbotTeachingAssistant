import unittest
from unittest.mock import patch, MagicMock

# Import updated CRUD methods
from backend.database.postgres import (
    create_user_course,
    read_users_for_course,
    delete_user_course,
    delete_user_courses_by_course
)

class TestUserCoursesCrudOps(unittest.TestCase):

    # ------------------------------------------------------------------
    # Tests for create_user_course
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_create_user_course_success(self, mock_get_db_connection):
        """
        Test a successful insertion into user_courses.
        rowcount == 1 indicates a new row was inserted.
        """
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Simulate rowcount = 1 => new record was inserted
        mock_cursor.rowcount = 1

        result = create_user_course('course-uuid-123', 'user-uuid-456')
        self.assertTrue(result)
        mock_get_db_connection.assert_called_once()

        insert_query = """
            INSERT INTO user_courses (course_id, user_id)
            VALUES (%s, %s)
            ON CONFLICT (course_id, user_id) DO NOTHING
        """
        mock_cursor.execute.assert_called_once_with(
            insert_query,
            ('course-uuid-123', 'user-uuid-456')
        )
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_create_user_course_conflict(self, mock_get_db_connection):
        """
        Test the scenario where the record already exists, causing rowcount == 0.
        This should return False since no new record was inserted.
        """
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # rowcount = 0 => conflict or already exists => no new insertion
        mock_cursor.rowcount = 0

        result = create_user_course('course-uuid-123', 'user-uuid-456')
        self.assertFalse(result)

        mock_get_db_connection.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_create_user_course_db_connection_failure(self, mock_get_db_connection, mock_log_error):
        """Test DB connection failure for create_user_course."""
        mock_get_db_connection.return_value = None

        result = create_user_course('course-uuid-123', 'user-uuid-456')
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()

        mock_log_error.assert_called_once_with("Failed to connect to the database.")

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_create_user_course_exception(self, mock_get_db_connection, mock_log_error):
        """Test exception scenario during insertion."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Insert error')
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = create_user_course('course-uuid-123', 'user-uuid-456')
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()
        mock_conn.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

        mock_log_error.assert_called_once_with("Error creating user course: Insert error")

    # ------------------------------------------------------------------
    # Tests for read_users_for_course
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_read_users_for_course_success(self, mock_get_db_connection):
        """
        Test returning user IDs for a course. Should return a list of user_id strings.
        """
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        # Suppose we have two rows with 'user_id' keys
        mock_cursor.fetchall.return_value = [
            {'user_id': 'user-uuid-111'},
            {'user_id': 'user-uuid-222'}
        ]
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        user_ids = read_users_for_course('course-uuid-123')
        self.assertEqual(user_ids, ['user-uuid-111', 'user-uuid-222'])

        mock_get_db_connection.assert_called_once()
        select_query = """
            SELECT user_id FROM user_courses WHERE course_id = %s;
        """
        mock_cursor.execute.assert_called_once_with(select_query, ('course-uuid-123',))
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.get_db_connection')
    def test_read_users_for_course_no_result(self, mock_get_db_connection):
        """
        Test returning an empty list when no user is found for the course.
        """
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        user_ids = read_users_for_course('course-uuid-999')
        self.assertEqual(user_ids, [])

        mock_get_db_connection.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_read_users_for_course_exception(self, mock_get_db_connection, mock_log_error):
        """
        Test returning an empty list upon exception.
        """
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Select error')
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        user_ids = read_users_for_course('course-uuid-888')
        self.assertEqual(user_ids, [])
        mock_get_db_connection.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

        mock_log_error.assert_called_once_with("Error retrieving users for course course-uuid-888: Select error")

    # ------------------------------------------------------------------
    # Tests for delete_user_course
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_delete_user_course_success(self, mock_get_db_connection):
        """
        Test deleting a user-course combination by course_id and user_id.
        """
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = delete_user_course('course-uuid-123', 'user-uuid-456')
        self.assertTrue(result)
        mock_get_db_connection.assert_called_once()

        delete_query = """
            DELETE FROM user_courses WHERE course_id = %s AND user_id = %s;
        """
        mock_cursor.execute.assert_called_once_with(delete_query, ('course-uuid-123', 'user-uuid-456'))
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_delete_user_course_db_connection_failure(self, mock_get_db_connection, mock_log_error):
        """Test DB connection failure for delete_user_course."""
        mock_get_db_connection.return_value = None

        result = delete_user_course('course-uuid-111', 'user-uuid-999')
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()
        mock_log_error.assert_called_once_with("Failed to connect to the database.")

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_delete_user_course_exception(self, mock_get_db_connection, mock_log_error):
        """Test exception scenario for delete_user_course."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Delete error')
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = delete_user_course('course-uuid-111', 'user-uuid-999')
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()
        mock_conn.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

        mock_log_error.assert_called_once_with("Error deleting user course: Delete error")

    # ------------------------------------------------------------------
    # Tests for delete_user_courses_by_course (new method)
    # ------------------------------------------------------------------
    @patch('backend.database.postgres.get_db_connection')
    def test_delete_user_courses_by_course_success(self, mock_get_db_connection):
        """Test deleting all user-course associations for a given course."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = delete_user_courses_by_course('course-uuid-123')
        self.assertTrue(result)
        mock_get_db_connection.assert_called_once()

        delete_query = """
            DELETE FROM user_courses WHERE course_id = %s;
        """
        mock_cursor.execute.assert_called_once_with(delete_query, ('course-uuid-123',))
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_delete_user_courses_by_course_db_connection_failure(self, mock_get_db_connection, mock_log_error):
        """Test DB connection failure for delete_user_courses_by_course."""
        mock_get_db_connection.return_value = None

        result = delete_user_courses_by_course('course-uuid-999')
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()
        mock_log_error.assert_called_once_with("Failed to connect to the database.")

    @patch('backend.database.postgres.logging.error')
    @patch('backend.database.postgres.get_db_connection')
    def test_delete_user_courses_by_course_exception(self, mock_get_db_connection, mock_log_error):
        """Test exception scenario for delete_user_courses_by_course."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Delete error')
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        result = delete_user_courses_by_course('course-uuid-999')
        self.assertFalse(result)
        mock_get_db_connection.assert_called_once()
        mock_conn.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

        mock_log_error.assert_called_once_with("Error deleting user courses by course_id 'course-uuid-999': Delete error")


if __name__ == '__main__':
    unittest.main()