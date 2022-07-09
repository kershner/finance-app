goto comment
Hello!  On Windows machines, once you setup a virtual environment and install the 
project's requirements, you can simply double click this batch file at any time to 
run this app.
:comment

set CURRENT_PATH=%cd%
cd..
set PARENT_PATH=%cd%
set VENV_PATH=%parent_path%\venv\Scripts
set DEV_SERVER_URL=http://localhost:8000/

rem Open browser to dev server URL and start server
start %DEV_SERVER_URL% && %VENV_PATH%\python %CURRENT_PATH%\manage.py runserver