===========
 PyEnvFile
===========

Install
=======
::

   pip install pydotenv

Usage
=====
::

   env = pydotenv.Environment()
   env['MY_VARIABLE'] = 'some-value'


 Check if file exists: pass `check_file_exists=True` to get an
 exception if the file does not exist. By default(`False`) the file is
 created.
