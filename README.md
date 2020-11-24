# Parsing Polar Bear Data with Python and Django
This is a demonstrator app focusing on different ways to use python and flask to parse data for a web application using polar bear tracking data. 

The goal of 'deliberate practice' is to think about how you'd solve this challenge, and to work at developing code to make this work. There is no single 'correct' version of this code. The purpose of the exercise it become familiar with different ways of making the application work. You should explore how this simple application is done in python with flask and sqlite3 so that you understand how the components work together to show up in the views you see in the browser.

Under 'deliberate practice' we offer up the challenge, then think about options for developing a solution, and code for 12 minutes. After that we pause to discuss how people are approaching the problem, and what they're trying to do. This should be repeated three times and then wrapped up with time for people to express what they found most useful during the session. This should take an hour.

Step 1) We'll use data on Polar bears in Alaska to develop our application Data is taken from https://alaska.usgs.gov/products/data.php?dataid=130 Download the zip file and unpack it to a folder. This will give us more data than we need, but that's ok. We're only using it to learn how to import data.

#### Table Relationships for the Data

We'll import data from two related tables. Each polar bear is listed in the USGS_WC_eartag_deployments_2009-2011.csv file. Each subsequent sighting of a bear is recorded in the USGS_WC_eartags_output_files_2009-2011-Status.csv file. The DeployID column in the second file references the BearID column in the first file. Therefore we end up with a one_to_many relationship between the two files. 

We are not using all of the columns that are here. We could use all of the data, but as we're not biologists, we'll only take what looks interesting to us. You can see the table structure in the parse_csv.py file where we create the tables.

Step 2) We can start developing our application to display the data. Create a new project folder called 'polar_bears' and then cd into the folder via the terminal and execute these commands:

        pyenv local 3.7.0 # this sets the local version of python to 3.7.0
        python3 -m venv .venv # this creates the virtual environment for you
        source .venv/bin/activate # this activates the virtual environment
        pip install --upgrade pip [ this is optional]  # this installs pip, and upgrades it if required.

We will use Django (https://www.djangoproject.com) as our web framework for the application. We install that with 
        
        pip install django

And that will install django version 3.1.3 with its associated dependencies. We can now start to build the application.

Now we can start to create the site using the django admin tools. Issue this command, and don't forget the '.' at the end of the line, which says 'create it in this directory'. This will create the admin part of our application, which will sit alongside the actual site. 

        django-admin startproject mysite .

We're using the name 'mysite' but you could use whatever seems appropriate. We'll save the temperature-stories' label for later in the app. For now we're setting up the support structure for the site, which will live in a separate folder.

We need to specify some settings for the site, which we do in the mysite/settings.py file. Open this and add this line above the line for pathlib import Path:

        import os

Now go to the end of the file to add a line specifying the root directory for the static files.

        STATIC_ROOT = os.path.join(BASE_DIR, 'static')

Now go further up the file to 'ALLOWED_HOSTS' so that we can run this beyond 'localhost' and 127.0.0.1, which are the only allowed ones if this is empty. Modify this accordingly to suit your needs:

        ALLOWED_HOSTS = ['word-otherword.herokuapp.com', 'localhost']

We now need to configure the database, which you saw was already detailed in the settings.py file. As django has a built-in admin tool, it already knows some of the tables that it needs to use. We can set this up with the command:

        python3 manage.py migrate

You should see a number of steps being run, each hopefully ending ... OK
If not, then look to the errors in the terminal. If you see one that says 'NameError: name 'os' is not defined', then go back and add the import for the 'os' library.

## Start the Server

We so this using the manage.py command tool by entering this command in the terminal:

        python3 manage.py runserver

If you're doing this on another platform, then you might need to use this instead (change the port number from 8000 as required):

        python3 manage.py runserver 0.0.0.0:8000 

If it went well, then you should see the python rocket launching your site. 

## Modelling our Data
The goal is to have the polar bear details on the website, which means we need to put the spreadsheet data into a database. This means creating models that map to tables in the database using Django's object relational mapping library.

We can now set about creating the space for our polar bear content by running this command:

        python3 manage.py startapp bears

This will create a new folder 'bears' containing relevant config files for us including space for database migrations, and other details specific to our content. 

we need to modify the settings.py file in the mysite app, so that it knows to include the 'bear' contents. We do this by adding a line in the section on 'INSTALLED_APPS'. Add this line to the end of the block ( plus the , at the end of the line above it).

        'bears.apps.BearsConfig',

Now we can open 'bears/models.py' and start adding the schema for our tables.

