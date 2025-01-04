#!/usr/bin/python3
"""
Contains the TestStateDatabaseClass
"""
import unittest
import os
from models.state import State
from models import storage
import MySQLdb


class TestStateDatabaseClass(unittest.TestCase):
    """Test cases for State class with DB storage"""

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                    "Skip if not using db storage")
    def test_create_state_db(self):
        """Test creating a state adds a record to database"""
        # Setup - get initial count
        conn = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST', 'localhost'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM states")
        initial_count = cur.fetchone()[0]
        
        # Action - create new state
        new_state = State(name="California")
        new_state.save()
        
        # Assert - check count increased
        cur.execute("SELECT COUNT(*) FROM states")
        final_count = cur.fetchone()[0]
        self.assertEqual(final_count, initial_count + 1)
        
        # Cleanup
        cur.close()
        conn.close()

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                    "Skip if using db storage")
    def test_create_state_file(self):
        """Test creating a state with file storage"""
        new_state = State(name="California")
        new_state.save()
        self.assertIn(new_state, storage.all(State).values())
