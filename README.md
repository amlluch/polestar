<H1>Polestar Assignment</H1>

Docker installation:

1) <strong>Build docker image:</strong> docker-compose build

2) <strong>Run docker for creating user and database:</strong> docker-compose up

3) <strong>Migrate database:</strong> docker-compose run --rm polestar /bin/bash -c "cd polestar; ./manage.py migrate"

4) <strong>Migrate restapi app database (if necessary):</strong><br>
docker-compose run --rm polestar /bin/bash -c "cd polestar; ./manage.py makemigrations restapi"<br>
docker-compose run --rm polestar /bin/bash -c "cd polestar; ./manage.py migrate restapi"<br>

Now you can run in a docker and play. If you want to change the postgres user and postgres passowrd change it inside config/db/database_env (before building the docker image).

The docker image uses gunicorn on port 8000

Ship codes are assumed to be 7 digit numbers. To import position data http://localhost:8000/api/import. 
During the import process the erroneous elements are discarded showing a list of those discarded in the response. 
The import process uploads a file that it deletes once the process has finished.

You can import files inside the container: <strong>docker-compose run --rm polestar /bin/bash -c "cd polestar; ./manage.py import path-to-file-to-import"</strong>. You can import as many files as you want at same time (more options with --help).

In the endpoint of the list of ships (api/ships) a "post" has been added to register ships. 
This post checks that the code is correct and that the boat does not exist.

The restapi app is the one that contains the models and a class for importing the data. This class is in utils.py  
The tests are also in the restapi app. It performs tests on different classes and tests several gets and posts. 
It also tests the import process using a file with data hosted in media/import/tests. 
To check just run "<strong>python3 manage.py test</strong>" in the root directory of the project (in a virtual environment).

You can see the route the ships have taken at http://localhost:8000



