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

We can now take the downloaded polar bear data and put the 'PolarBear_Telemetry_southernBeaufortSea_2009_2011' folder and its' files under the 'bears' folder. We'll need this later when we load the data into the database.

we need to modify the settings.py file in the mysite app, so that it knows to include the 'bear' contents. We do this by adding a line in the section on 'INSTALLED_APPS'. Add this line to the end of the block ( plus the , at the end of the line above it).

        'bears.apps.BearsConfig',

Now we can open 'bears/models.py' and start adding the schema for our tables. We'll start by adding a model for the bears. There is a lot of info in the csv file, but we'll only focus on the basics. Add the missing lines so that your file looks like this:

        from django.conf import settings
        from django.db import models
        from django.utils import timezone

        # Create your models here.

        class Bear(models.Model):
            bearID = models.IntegerField()
            pTT_ID = models.IntegerField()
            capture_lat = models.FloatField()
            capture_long = models.FloatField()
            sex = models.TextField()
            age_class = models.TextField()
            ear_applied = models.TextField()
            created_date = models.DateTimeField(auto_now_add=True)

            def __str__(self):
                return self.bearID, self.pTT_ID, self.capture_lat, self.capture_long, self.sex, 
                self.age_class, self.ear_applied, self.created_date

Now we nee to generate a migration file for Django to use when it loads the model into the schema. By having Django do this, it will generate the correct SQL needed for our database. The timestamp will be generated automatically for us for each new entry.

First, we ask Django to generate the migration file with the command:

        python3 manage.py makemigrations bears

This will read the models.py file and generate a migration file based on changes found there. 

Second, we run the generated migration with the command:

        python3 manage.py migrate bears

Now we have the migration done and the table is created in our database, and we can load our data into the database. We do this using Django's admin commands, which provide access to the models, and thus the database for us. See more here: https://docs.djangoproject.com/en/3.1/howto/custom-management-commands/ 

Under the 'bears' app create a folder 'management' and inside that create another one named 'commands'. Then create a file parse_csv.py in that folder. Put this code into that file:

        import csv
        import os
        from pathlib import Path
        from django.db import models
        from django.core.management.base import BaseCommand, CommandError

        from bears.models import Bear

        class Command(BaseCommand):
        help = 'Load data from csv'

        def handle(self, *args, **options):

            # drop the data from the table so that if we rerun the file, we don't repeat values
            Bear.objects.all().delete()
            print("table dropped successfully")
            # create table again

            # open the file to read it into the database
            base_dir = Path(__file__).resolve().parent.parent.parent.parent
            with open(str(base_dir) + '/bears/PolarBear_Telemetry_southernBeaufortSea_2009_2011/USGS_WC_eartag_deployments_2009-2011.csv', newline='') as f:
                reader = csv.reader(f, delimiter=",")
                next(reader) # skip the header line
                for row in reader:
                    print(row)

                    bear = Bear.objects.create(
                    bearID = int(row[0]),
                    pTT_ID = int(row[1]),
                    capture_lat = float(row[6]),
                    capture_long = float(row[7]),
                    sex = row[9],
                    age_class = row[10],
                    ear_applied = row[11],
                    )
                    bear.save()
            print("data parsed successfully")

With this we can drop the data from the table, and then load it in, as required. We don't use any libraries for this as we want to pull specific fields from the file.

## Creating Views
We can now create views for our data so that we can see all of the bears, plus also each individual one.

Open mysite/urls.py and add 'include' to the import list, and add the second line as well below the one for 'admin.site.urls':

        from django.urls import path, include

        path('', include('bears.urls')),

This tells our application to look for content in the 'bears' app. 

Next go into the 'bears' folder and create an empty 'urls.py' file for us to manage the available views in the app. To start with put this into the file:

        from django.urls import path
        from . import views

        urlpatterns = [
        path('', views.bears_list, name='bear_list'),
        ]

We can now open 'bears/views.py' to add the view. At the

        def bear_list(request):
                bears = Bear.objects.all()
                return render(request, 'bears/bear_list.html', {'bears' : bears})

Next, we need to create the actual html page to display. As before, create a 'templates' folder under 'bears' and then another 'bears' folder under that. Then create a file at 'bears/templates/bears/bear_list.html' which has this simple code:

        <html><head>
        <title>Polar Bear Tracking</title>
        </head><body>
            <h1>Polar bears Tagged for Tracking</h1>
            {% for bear in bears %}
             <b> <a href={%url_for('bear', bear_id= bear.id }}>{{bear.bearID }}</a></b>
            This is a {{ bear.age_class }} aged bear 
            {{bear.bearID}}, a {{ bear.sex }} bear, who has has an tag in its' {{ bear.ear_applied }} ear, with {{ bear.pTT_ID }} devise, and was
            tagged at {{ bear.capture_lat }} and {{ bear.capture_long }}
            </p>
            {% endfor %}
        </body></html>

Showing the full list, is a start, but it would be better to also show individual bears, so that later we can add the data for their sightings from the other csv file. We do that with a few steps.

First, add a link to indivual bears on the bear_list.html page around 'Bear' like this:

         <b> <a href="{% url 'bear_detail' id=bear.id %}">{{bear.bearID }}</a></b>

This will link the bear_detail page to the bear.id value, which we'll pass too the query for the page.

Second, we add a line in bears/urls.py for the view, which follows the one for the list:

        path('bear/<int:id>/', views.bear_detail, name= 'bear_detail'),

This tells the view to expect and integer as 'id' to be used in the query.

Third, we add some imports to help us, and add a view to the bears/views.py file:

        from django.shortcuts import render, get_object_or_404
        from .models import Bear

        def bear_list(request):
            bears = Bear.objects.all()
            return render(request, 'bears/bear_list.html', {'bears' : bears})

        def bear_detail(request, id):
            bear = get_object_or_404(Bear, id=id)
            return render(request, 'bears/bear_detail.html', {'bear' : bear}
        
Note, the import for 'get_object_or_404' at the top. Then we use this to query for the details of the bear.

Fourth, is adding a new file to display the code at templates/bears/bear_detail.html with this code:

        <html><head>
        <title>Individual Polar Bear Tracking</title>
        </head><body>
            <h1>Polar Bear Tagged for Tracking</h1>
            <p>Bear: 
                <b>{{bear.bearID }}</b> | 
                {{bear.pTT_ID}} | 
                {{ bear.capture_lat}} | 
                {{bear.capture_long}}	| 
                {{bear.sex}} |
                {{ bear.age_class}} |
                {{bear.ear_applied}}	
            </p>
            <p>Sightings via Radio Device</p>
        </body></html>
        
Now you can reload the page, and you should be able to see the individual bear details page. 

Finally, we're ready to do some more work with this so that we can add the sightings from the other table and show them on the bear detail page.

### Adding a second table

The file ending with ...status.csv holds details for sightings of bears, so that you could see where and when their radio transmitters were noticed. Again, we're only interested in some columns from the file.

 deployID INTEGRER, recieved TEXT, latitude REAL, longitude REAL, temperature REAL, deployment_id INTEGER

This will give us a table that references the deployments table via the deployment_id column, and let us show all sightings of a bear on the same page.

You can add more details to the parse_csv.py file to read the status.csv file in, and to store the details into a new 'status' table in a similar manner as before.

******************************************************
**** The data is messy and the parsing will break ****
******************************************************

When you run this new method you will find the parsing breaks due to gaps in the data. It broke because one of the cells had no data, or had the data format different from what the parser was expecting. This is the nature of real-world data. It's not always nice and tidy.

Given we're only parsing this data as an exercise, you can find the broken cell, and then you can either 
1. delete the row, and then re-run the parse_csv command, or 
2. write a few lines of code as an 'if/else' statement to check the value of the cell and to either ignore it, or do something else as required to make it work.

For simplicity here, you can just delete the row and move on so that you get the file imported and the page views showing. You can see the start of this work if you switch to the 'solution' branch of this repository and look at the parse_csv.py file there. You'll find the solution branch in the drop-down menu at the top of the file listing on the left.

You need to modify the parse_csv file some more. You do this you need to 'look up' the ID of each bear in the 'deployment' table (which we're calling 'bears) in order to reference this in each 'status' table (which we're calling 'sighting') instance. You can do this with a few lines like this:

        bear_temp = row[0]
            print(bear_temp)
            bear = Bear.objects.filter(bearID = bear_temp).first()
        ...
        bear_id = bear,

We do this in order to ensure that each 'Status' is tied correctly to a 'Deployment'.

This is rough and ready, and is messy, but then so too is the data that we're working with here.

This works, but also shows issues. For example, BearID 20414 appears twice in bears. If you select the second one, then you have no connected sightings. If you pick the first one, then you have LOTS of sightings.

From here you could show the locations of the sightings on a map using the GPS coordinates. You could also do a chart showing how many sightings there were for each bear by date. You could also do something with the other categories to produce visualisations to suit your needs.





    


