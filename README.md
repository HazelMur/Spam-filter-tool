# Spam-filter-tool

Pre-requirements 

1.	Install MySQL server to your computer. https://dev.mysql.com/downloads/mysql/ 
2.	Create a local database

Setup Backend

1.	Install hMailServer
Setup a domain called “@test.com”. 
Setup test account:
-	test@test.com
-	test2@test.com
-	test3@test.com
-	admin@test.com

2.	Install Thunderbird
Thunderbird will be used as the email client.
You need to login to thunderbird using the following settings for each account:

3.	Install MySQL Workbench
This tool is used to host and display the database for the application.

Setup Web Application

1.	Download code
You can download all the code needed on GitHub: https://github.com/HazelMur/Spam-filter-tool.git 

2.	Create a virtual environment (https://docs.python.org/3/library/venv.html)
Enter the following commands in the command line to create and activate your virtual environment:
	py -3 -m venv venv
	venv\Scripts\activate

3.	Navigate to the directory.
In the command line navigate to the directory where the “requirement.txt” file is located.
Enter “pip install reguirements.txt”

4.	Edit the _init_.py file
In the user’s folder edit the _init_.py file
Edit the database credentials to suit your database you have created.

To update these changes, in the command line enter the following commands:
	flask db migrate -m (Migrating models to local database)
	flask db upgrade

5.	Run the flask application
Finally, run the flask application.
Enter “flask run” in the command line and when you enter http://127.0.0.1:5000/ on your web browser the flask app should appear. 
