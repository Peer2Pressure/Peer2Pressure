# Peer2Pressure


## About

This document contains information on how to setup up, run and deploy the peer2pressure app.

- [API Documentation](https://p2psd.herokuapp.com/swagger)
- [Frontend documentation](https://github.com/Peer2Pressure/Peer2Pressure/blob/main/frontend/README.md) 

## Prerequisites
- git
- Python 3.9
- Node.js
- npm

Clone the repo:
```sh
git clone https://github.com/Peer2Pressure/Peer2Pressure.git
```

Create a virtual environment
```sh
cd Peer2Pressure
python3 -m venv .venv
source .venv/bin/activate
```

Install python dependiencies
```sh
pip3 install -r backend/requirements.txt
```

For frontend development, install react dependencies
```sh
cd frontend && npm install
```

## Running Django App

In order to run the app locally, you need to migrate the database changes. You can also optionally create a super user to access the admin page.
```sh
cd backend
python3 manage.py migrate
python3 manage.py createsuperuser
```

#### Run the app
```sh
python3 manage.py runserver
```

The app can be accessed at http://localhost:8000.

Go to http://localhost:8000 and click `Join Now` to create a new account. Once the account is created you will need to activate this account through admin panel. To activate a user,

- Go to http://localhost:8000/admin
- Select the Users model.
- Select the user you signed up with.
- Check the `active` checkbox and save.

#### Setting Up Nodes
Once you have activated your user you will need to resgister you current localhost as one of your node is handle authentication in the frontend. This step can be done directly through the admin panel.

Follow these commands to achieve this:
```sh
ENDPOINT="http://localhost:8000"
TOKEN=$(echo <your_username>:<your_password> | base64)
curl -X POST -H "Content-Type: application/json" "http://localhost:8000/nodes/" -d '{"api_endpoint": "'"$ENDPOINT"'", "token": "'"$TOKEN"'"}'
```

In order to delete a node:
```sh
curl -X POST -H "Content-Type: application/json" "http://localhost:8000/nodes/" -d '{"api_endpoint": "'"$ENDPOINT"'"}'
```

Once these steps are complete you will be able to login to to your user account through http://localhost:8000.


## Development

Once you run the app you will be able to to see real time changes to the Django app.

In case, you want to develop the frontend using the React app, follow these steps.

Run react app
```sh
cd frontend
npm start
```

This will open a new browser page at http://localhost:3000.

***Note:** The user will have to be logged in through https://localhost:8000 for the app to make successful api calls as the login is handled by Django*

All react updates will be reflected in the app realtime.

Once all updates are completed, you can build the staticfiles and move it to the `backend/` folder so that only one app needs to be run. Run the following command to achieve this:
```sh
npm run relocate
```

## Deployment

#### Deploying on Heroku

Create a heroku app and add `BASE_HOST` config variable. `BASE_HOST` is the endpoint of your herokuapp. You can add this by going to the settings tab of your heroku app. Example: `https://<YOUR_APP_NAME>.herokuapp.com`. You need to include the scheme.

Login and add the url to git remote. You will need to install heroku cli for this step.


```sh
heroku login
git remote add heroku https://git.heroku.com/<YOUR_APP_NAME>.git
```

Deploy app to main branch of heroku. Use the command below to deploy just the Django app to heroku from any dev branch. Make sure you have relocated the react static files from frontend usign `npm run relocate` if you have made any frontend changes.
```sh
git add .
git commit -m "Deploy to heroku"
git push heroku `git subtree split --prefix backend/ <YOUR_BRANCH_NAME>`:refs/heads/main
```

Once this is completed you will need to migrate the model changes on heroku and also create a superuser.
```sh
heroku run --app <YOUR_APP_NAME> python manage.py migrate
heroku run --app <YOUR_APP_NAME> python manage.py createsuperuser
```

Register your node using the steps mentiond [here](#setting-up-nodes). Update `https:localhost:8000` to your heroku app `BASE_HOST`.

