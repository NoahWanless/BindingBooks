#################################### Project Overview: ####################################

The Project goal was to create a service that facilitates the purchase, reading, and review of books, 
all the while allowing for safe and fun community interaction.

We decided to do this project because books! we love them ​and wanted to make a project around them.
We also wanted to create an integrated system with many through lines between individual parts giving us a good challenge​ of a project,
giving us a chance to improve our teamwork skills.
We also wanted a project that gave us chances to develop skills outside of Django.
This was also done as a final for our Introduction to Web App Development class

Feature List:
1) accounts
2) book purchasing, browsing, and reading and reviews
3) forum posting
4) content moderation (profanity filter)
5) stripe payment integration
6) AWS hosting (not visable from this github but we did it)
7) yaml scripts to upload books
8) And more, explore the code to find more!

Some areas for improvment:

1) More BIG user features​
2) Better styling​

Key resources, services and skills gained in:
1) Django framwork
2) Stripe
3) AWS (EC2 instance using ubuntu OS system using gunicorn and nginx for the server)
4) yaml scripts




#################################### Details on how to run: ####################################

Additionally all the commands i put will be off of unix based stuff as i dont know powershell, but its mostly similar
Firstly we are going to assume that you have copied this into a new directory, if not, skip ahead most of these steps.

Firsly after copying the github into you directory, youll need to set up your vitrual enviroument with this command:
(NOTE: that all these commands should be run in the highest level directory of the project unless i make specfic note otherwise)

python3 -m venv .venv              (just python for powershell users)

Next you want to activate your enviroument:

source .venv/bin/activate            (running simply 'deactivate' will deactivate it)

Next you need to install all the packages that we used here, do so by running this command:

pip install -r requirements.txt

From here the last remaining step will be to create a .env file in the highest level directory of the project. Within it place the following line:

stripe_fake_checkout=True        (this skips a level of security that needs access to my personal stripe account to confirm user purchases)

Now we are ready to start the website. First run:

python3 manage.py makemigrations

Then:

python3 manage.py migrate

        # These have a chance to break, if they do, for example saying that certain dependencies dont exist try one of or a combination of the folloing
        # 1) Delete the db.sqlite3 file
        # 2) Delete all migration files within each 'app' that exist within the files called 'migrations' however dont delete the '__init__.py' file
        # 3) run 'python3 manage.py flush' *NOTE this will remove everything in the database so you will have to recreate stuff*

Now that the database is ready, its time to get some sample books from our yaml scripts:

python3 manage.py fetch_books --query=fiction --count=30           (again remember that no 3 for powershell users)

----------------- From here its time to actually run the project: -----------------
(if you already had the project set up before hand youd start here)
To run, run this command (make sure your in the highest level directory of the project):

python3 manage.py runserver

This starts the local server and provides you a url to put in your browser.

From here nagiating the site should be easy but some final things of note:

        # 1) Remember the /admin site exists (needs a superuser)
        # 2) If you need to make a super user the command is 'python3 manage.py createsuperuser'
        # 3) To access the moderation queue on the site you need to be loged in as a super user
        # 4) Its possible some package was missed in the requirements, if so itll throw you an error
             and tell you want thing is missing, from there just install it and you should be fine.

Some final Stripe notes:

If you go to purchase something, you need to make sure the item your purchasing (through the admin view) is set up correctly and has:
i) A valid stripe ID the only one being this one: 'prod_TOqGRRWcrlobWC'
ii) A price of 10 dollars (as this is what it is on the stripe side)

To purchase use this info: 
i) The CV number is any 3 digit number 
ii) The mouth date just needs to be any date in the future, like '12/28' (as of the time of writing this is in the future at least)
iii) 4242 4242 4242 4242 for the card number
iv) Also for like billing info 77777 will work, any 5 digit number works.

And that should be it! I would suggest highly as well that you actually do a test run of all this to ensure everything is working before you show it off.

Also i am unsure if the stripe stuff might one day just decide to turn off, so who knows, again test before you show off.




#################################### Additionaly stripe stuff: ####################################
(This is for me (Noah) only as all you guys dont have the stripe login info for the cli to do this)

To set up the 'webhook' listener thing for 'extra confirmation' on purchases
Open a new and different terminal then what your running the website in and run this command:

stripe listen --forward-to localhost:8000/payments/webhooks/stripe/

Make sure in your .env file this is set to False:

stripe_fake_checkout=False

stripe logs tail          <--this displays api messages post/gets that stripe gets

And that should be it!





