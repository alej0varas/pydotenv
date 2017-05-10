from unittest import TestCase
import tempfile
import os

from pydotenv import Environment


class EnvironmentTestCase(TestCase):
    does_not_exist = 'does_not_exist'

    def setUp(self):
        self.dot_env = tempfile.NamedTemporaryFile()
        self.dot_env.write(b'k=v')
        self.dot_env.write(b'\n')
        self.dot_env.write(b'q="b"')
        self.dot_env.seek(0)

    def test_backup_file(self):
        tmp_file = tempfile.TemporaryFile()
        env = Environment(tmp_file.name)

        self.assertTrue(os.path.isfile(env.backup_file_name))

    def test_create_if_not_exist(self):
        env = Environment(self.does_not_exist)

        self.assertTrue(os.path.isfile(env.backup_file_name))

        os.remove(self.does_not_exist)

    def test_item_assignment(self):
        env = Environment(self.dot_env.name)
        env['k'] = 'nv'

        self.dot_env.seek(0)
        self.assertEqual(self.dot_env.read().decode(), 'k=nv\nq="b"\n')

        env['nk'] = 'v'

        self.dot_env.seek(0)
        self.assertEqual(self.dot_env.read().decode(), 'k=nv\nq="b"\nnk=v\n')

        # Keep quotes(")
        env['q'] = 'nb'

        self.dot_env.seek(0)
        self.assertEqual(self.dot_env.read().decode(), 'k=nv\nq="nb"\nnk=v\n')

    def test_load_environment(self):
        env = Environment(self.dot_env.name)

        result = env.load_environment()

        self.assertEqual(result[0], 'k=v\n')
        self.assertEqual(result[1], 'q="b"')

    def test_skip_if_key_not_equal(self):
        self.dot_env.seek(0)
        self.dot_env.write(b'ook=v\n')
        self.dot_env.write(b'ok=v\n')
        self.dot_env.seek(0)
        env = Environment(self.dot_env.name)

        env['ok'] = 'nv'

        self.dot_env.seek(0)
        self.assertIn(b'ok=nv', self.dot_env.read())
        self.dot_env.seek(0)
        self.assertIn(b'ook=v', self.dot_env.read())

    def test_unset_key(self):
        env = Environment(self.dot_env.name)

        env['k'] = None

        self.dot_env.seek(0)
        self.assertIn(b'# k=v', self.dot_env.read())

    def test_dont_process_lines_without_equal(self):
        self.dot_env.write(b'# ckv\n')
        self.dot_env.seek(0)
        env = Environment(self.dot_env.name)

        env['ck'] = 'nv'

        self.dot_env.seek(0)
        self.assertIn(b'# ckv\n', self.dot_env.read())
        self.dot_env.seek(0)
        self.assertIn(b'ck=nv', self.dot_env.read())

    def test_items(self):
        env = Environment(self.dot_env.name)

        result = env.items()

        self.assertEqual(result, [('k', 'v'), ('q', '"b"')])
