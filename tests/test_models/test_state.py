#!/usr/bin/python3
"""Unit test for testing MySQL storage with State model"""
import unittest
import os
import MySQLdb
from models.state import State
from models import storage


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 "Test only relevant for DB storage")
class TestDBStorageState(unittest.TestCase):
    """Tests for the State model with DB storage"""

    def setUp(self):
        """Set up the database connection and environment for tests"""
        self.db = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        self.cursor = self.db.cursor()

    def tearDown(self):
        """Clean up after tests"""
        self.cursor.close()
        self.db.close()

    def test_create_state(self):
        """Test creating a State via the console"""
        # Get initial count of states
        self.cursor.execute("SELECT COUNT(*) FROM states;")
        initial_count = self.cursor.fetchone()[0]

        # Create a new State
        new_state = State(name="California")
        storage.new(new_state)
        storage.save()

        # Get updated count of states
        self.cursor.execute("SELECT COUNT(*) FROM states;")
        updated_count = self.cursor.fetchone()[0]

        # Validate the difference is +1
        self.assertEqual(updated_count, initial_count + 1)


if __name__ == "__main__":
    unittest.main()
