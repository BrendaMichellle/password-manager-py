## All you need to know about venv in python

### What is it?

It is a self-contained directory tree that contains a Python installation for a particular version of Python, plus a
number of additional packages. The modules you install in your venv will not affect the global python installation on
your system.

### Why do we need it in this application?

This application uses number of python modules. Installing these globally will interfere with other modules you possibly
have in your system, to avoid this, we suggest you used a venv.

### How to?

Here is a small list of commands you will need:

1. **Create** a new venv named py-pass-venv: `python3 -m venv py-pass-venv`
    - Run this commands where you want your venv to be created.
2. **Activate** your venv:
    - On Windows, run:<br>
      `py-pass-venv\Scripts\activate.bat`
    - On Unix or MacOS, run:<br>
      `source tutorial-env/bin/activate`
3. **Install packages** from the `requirements.txt` provided:
    - `python -m pip install -r requirements.txt`
4. (For development) **Export** a list of packages:
    - `pip freeze > requirements.txt`
