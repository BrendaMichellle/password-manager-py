## Tkinter-based-gui:

### Pre-requisites:

1. Install Python 3.
2. Install the requirements ([you can find them here](pass-manager-tkinter/requirements.txt)) into a virtual python
   environment.
    - Instructions on how to create one and install the requirements can be
      found [here](https://docs.python.org/3/tutorial/venv.html)
3. Clone the repo. [Optional] Use the release branch for Beta features!
4. Optional (but recommended!): Set 2 environment variables on your system:
    - PY_PASS_MGR_USER: This will be the master username for the application.
    - PY_PASS_MGR_PASS: This will be the master password for the application.

### How to run:

1. Activate the venv for your session:
    - Windows: \path\to\venv\Scripts\activate.bat
    - Unix or MacOS: source /path/to/venv/bin/activate
2. Now, simply run the command: `python3 launcher.py`. Find this file [here.](pass-manager-tkinter/launcher.py)

### How to use:

1. The default username and password is: admin, admin.
    - (Ignore this if you have set the environment variables).
2. This can be changed [here.](pass-manager-tkinter/data/master.csv)
    - Note: If the environment variables are not set, the username and password from the csv will be used.

### Screenshots:

| Screen                  | Image                                                                                              |
|-------------------------|----------------------------------------------------------------------------------------------------|
| Login Screen            | ![Login Screen](screenshots/tkinter-gui/login_window.png "Login Screen")                           |
| Main Application Screen | ![Main App Screen](screenshots/tkinter-gui/main_app_window.png "Main App Screen")                  |
| Add a new password      | ![Add a new password](screenshots/tkinter-gui/add_new_password_window.png "Add a new password")    |
| List saved passwords    | ![List saved passwords](screenshots/tkinter-gui/list_passwords_window.png "List saved passwords")  |
| Generate a new password | ![Generate a password](screenshots/tkinter-gui/generate_password_window.png "Generate a password") |
