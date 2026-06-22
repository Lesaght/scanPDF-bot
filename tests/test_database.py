import unittest
from database.db import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Initialize an in-memory SQLite database to avoid disk pollution
        self.db = Database(db_path=":memory:", start_backup=False)

    def tearDown(self):
        self.db.close()

    def test_create_and_get_user(self):
        user_id = 12345
        code = "123456"
        lang = "ru"
        
        self.db.create_user(user_id, code, lang)
        user = self.db.get_user(user_id)
        
        self.assertIsNotNone(user)
        self.assertEqual(user['user_id'], user_id)
        self.assertEqual(user['code'], code)
        self.assertEqual(user['lang'], lang)
        self.assertEqual(user['verified'], 0)  # Default
        self.assertEqual(user['attempts'], 3)  # Default
        self.assertEqual(user['filter'], "filter_bw")  # Default
        self.assertEqual(user['quality'], 95)  # Default
        self.assertEqual(user['pdf_format'], "standard")  # Default
        self.assertEqual(user['notifications'], 1)  # Default

    def test_update_user_single_field(self):
        user_id = 54321
        self.db.create_user(user_id, "654321", "en")
        
        self.db.update_user(user_id, verified=1)
        user = self.db.get_user(user_id)
        self.assertEqual(user['verified'], 1)

    def test_update_user_multiple_fields(self):
        user_id = 99999
        self.db.create_user(user_id, "000000", "ru")
        
        self.db.update_user(
            user_id, 
            verified=1, 
            attempts=5, 
            filter="filter_sepia", 
            quality=85, 
            pdf_format="compressed", 
            notifications=0
        )
        
        user = self.db.get_user(user_id)
        self.assertEqual(user['verified'], 1)
        self.assertEqual(user['attempts'], 5)
        self.assertEqual(user['filter'], "filter_sepia")
        self.assertEqual(user['quality'], 85)
        self.assertEqual(user['pdf_format'], "compressed")
        self.assertEqual(user['notifications'], 0)

    def test_get_nonexistent_user(self):
        user = self.db.get_user(999)
        self.assertIsNone(user)

if __name__ == '__main__':
    unittest.main()
