
# Online Workspace

https://www.onlineworkspace.org

Web application to store and organise files, tasks and notes for different projects in their relevant 'workspaces',
and be able to share them with other users


## Features

- Each Workspace has tasks and folders, with each task having the ability to point to the relevant folder
- Files are uploaded and organised into their relevant folders, notes are created inside notebooks which are stored in their relevant folders alongside files
- Users can create as many tasks, notes, notebooks, and folders as they wish
- Users can also grant access to their workspaces to other users, allowing for a viable solution for handling group projects with an efficient way of sharing relevant files, notes and tasks in an organised manner as described above

  
## Roadmap

- Django channels for real time updates for all users in a workspace

- Ability to search through all items in a workspace

- Subscription based membership for unlimited workspaces and file uploads

- Option to limit freedom of specified users in a workspace

  
## User Guide

Please click the floating help button on the bottom right corner in any of the pages of the website to get a relevant rundown of what's possible in the current page


  
## Run Locally

Clone the project

```bash
  git clone https://github.com/kunheeha/onlineworkspace.git
```

Go to the project directory

```bash
  cd onlineworkspace/onlineworkspace
```

Open requirements.txt file and remove 'psycopg2==2.8.6' and save

(This is only required to use a postgresql database. If running locally to test, sqlite3 can be used instead)

(To use postgresql, uncomment the relevant code in settings.py under DATABASES, and remove the code for sqlite3)

Install requirements

```bash
  pip install -r requirements.txt
```

Open up setting.py file in the onlineworkspace folder and change the SECRET_KEY variable to a string of your choice

Start the server

```bash
  python manage.py runserver
```



  