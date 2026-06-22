import unittest
from utils.translations import get_translation, translations

class TestTranslations(unittest.TestCase):
    def test_translations_keys_match(self):
        # Ensure 'ru' and 'en' have the exact same keys
        ru_keys = set(translations['ru'].keys())
        en_keys = set(translations['en'].keys())
        self.assertEqual(ru_keys, en_keys, "Russian and English translation keys must be identical")

    def test_get_translation_non_existent_user(self):
        # Create a mock database that returns None for get_user
        class MockDbNonExistent:
            def get_user(self, user_id):
                return None
                
        # Non-existent user should default to 'ru' language
        start_text = get_translation(user_id=123, key='start', custom_db=MockDbNonExistent())
        self.assertEqual(start_text, translations['ru']['start'])

    def test_get_translation_ru_user(self):
        # Create a mock database that returns a user dict with lang='ru'
        class MockDbRu:
            def get_user(self, user_id):
                return {'lang': 'ru'}
                
        help_text = get_translation(user_id=123, key='help', custom_db=MockDbRu())
        self.assertEqual(help_text, translations['ru']['help'])

    def test_get_translation_en_user(self):
        # Create a mock database that returns a user dict with lang='en'
        class MockDbEn:
            def get_user(self, user_id):
                return {'lang': 'en'}
                
        help_text = get_translation(user_id=123, key='help', custom_db=MockDbEn())
        self.assertEqual(help_text, translations['en']['help'])

    def test_formatted_translation(self):
        class MockDbRu:
            def get_user(self, user_id):
                return {'lang': 'ru'}
                
        # The key 'code_message' requires code and attempts formatting
        formatted_text = get_translation(
            user_id=123, 
            key='code_message', 
            custom_db=MockDbRu(), 
            code='ABCDEF', 
            attempts=3
        )
        self.assertIn('ABCDEF', formatted_text)
        self.assertIn('3', formatted_text)

if __name__ == '__main__':
    unittest.main()
