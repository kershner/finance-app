# Finance by Month
<img src="https://djfdm802jwooz.cloudfront.net/static/project_images/0e3455cc05a340fea87230575ced49f5.png" width="400" height="400" />
This is an extremely lean monthly budgeting program.  It allows you to add monthly income/expense transactions and perform simple economic forecasts into the future, one month's budget at a time.
<br><br>
This app is basically just Django, JavaScript, and CSS (SASS).  It should be very easy to modify and mutate for your own purposes, should you wish.

# Running the app
There are three easy ways to run this app on your own machine:
- **With Docker**
  - If you've got Docker installed on your system it's as easy as pulling this repo, navigating to the directory, and running `docker-compose up`
  - The container will be built in around 15 seconds, and while it's running you'll be able to visit the site at `localhost:8020`
- **Use the run_app_win.bat batch script** (Windows only)
  - On Windows:
    - Pull this repo
    - Create a `venv` one directory up from the repo's code
    - Install the `requirements.txt`
    - Run `run_app_win.bat`
  - The Django dev server will start and your default browser will open to the site automatically
- **Pull the repo and run the Django development server**
  - You'll need to install the project's Python `requirements.txt`
