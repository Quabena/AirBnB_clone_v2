#!/usr/bin/python3
""" """
import os
import unittest
import MySQLdb
from tests.test_models.test_base_model import TestBasemodel
from models.state import State
from models import storage


class TestState(TestBasemodel):
    """Represents the tests for the State model."""
    def __init__(self, *args, **kwargs):
        """Initializes the test class."""
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """Tests the type of name."""
        new = self.value()
        self.assertEqual(
            type(new.name),
            str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        )

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                    "Skip if not using db storage")
    def test_create_state_db(self):
        """Test creating a state adds a record to database"""
        conn = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST', 'localhost'),
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cur = conn.cursor()
        
        # Get initial count
        cur.execute("SELECT COUNT(*) FROM states")
        initial_count = cur.fetchone()[0]
        
        # Create new state
        test_state = State(name="TestState")
        test_state.save()
        
        # Verify count increased
        cur.execute("SELECT COUNT(*) FROM states")
        final_count = cur.fetchone()[0]
        self.assertEqual(final_count, initial_count + 1)
        
        # Cleanup
        cur.close()
        conn.close()

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                    "Skip if not using db storage")
    def test_delete_state_db(self):
        """Test deleting a state removes record from database"""
        conn = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST', 'localhost'),
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cur = conn.cursor()
        
        # Create state to delete
        test_state = State(name="StateToDelete")
        test_state.save()
        
        # Get count before delete
        cur.execute("SELECT COUNT(*) FROM states")
        initial_count = cur.fetchone()[0]
        
        # Delete state
        storage.delete(test_state)
        storage.save()
        
        # Verify count decreased
        cur.execute("SELECT COUNT(*) FROM states")
        final_count = cur.fetchone()[0]
        self.assertEqual(final_count, initial_count - 1)
        
        # Cleanup
        cur.close()
        conn.close()
