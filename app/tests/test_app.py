class TestApp:
    def test_debug_is_true(self, config):
        assert config['DEBUG'] is True

    def test_reloader_is_true(self, config):
        assert config['USE_RELOADER'] is True

    def test_testing_is_true(self, config):
        assert config['TESTING'] is True

    def test_sqlite_is_db(self, config):
        assert config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///blog.db'
