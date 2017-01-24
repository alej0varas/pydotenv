import shutil
import tempfile
import os


class Environment:
    DEFAULT_FILE_PATH = '.env'

    def __init__(self, file_path=DEFAULT_FILE_PATH):
        self.file_path = file_path
        self.backup_file()

    def __setitem__(self, name, value):
        self.save_environment(name, value)

    def load_environment(self):
        with self.get_environment_file('r') as environment_file:
            environment = environment_file.readlines()
        return environment

    def save_environment(self, key, value):
        environment = self.load_environment()
        with self.get_environment_file('w') as environment_file:
            found = False
            for line in environment:
                new_line = line
                if not found and key in line and '=' in line:
                    _key, old_value = line.strip().split('=')
                    if key == _key:
                        found = True
                        # Keep quotes
                        if old_value[0] == old_value[-1] == '"':
                            value = '"' + value + '"'
                        if value is None:
                            new_line = '# ' + key + '=' + str(old_value) + '\n'
                        else:
                            new_line = key + '=' + str(value) + '\n'
                if not new_line.endswith('\n'):
                    new_line += '\n'
                environment_file.write(new_line)

            if not found:
                new_line = key + '=' + str(value) + '\n'
                environment_file.write(new_line)

    def get_environment_file(self, mode):
        return open(self.file_path, mode)

    def backup_file(self):
        self.validate_file_path()
        tmp_file = tempfile.NamedTemporaryFile(prefix='env-')
        tmp_file.close()
        self.backup_file_name = tmp_file.name
        shutil.copyfile(self.file_path, self.backup_file_name)

    def validate_file_path(self):
        if not os.path.isfile(self.file_path):
            open(self.file_path, 'w').close()


__version__ = '0.0.2'
