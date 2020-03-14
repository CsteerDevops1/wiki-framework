
## coreSerice

Database and API validation are automatically set from schema.json file.
Run `docker build -t flask . && docker run --name flask_api -d -p 5000:5000 flask` to start API, it needs MONGO_URI env variable to be set in .env. Of course it needs running mongo somewhere.

API documentation is on /api/wiki/doc, auto-generated with SwaggerUI.

API URL : /api/wiki

SERVES : POST, GET, PUT, DELETE

All the files can use environmental variables from .env file, create it in coreService/ if you want to debug something. It won't override existing variables with such names.
Tests won't work without this file. (or you can setup all of these by hands)

Example .env file : 

MONGO_URI="mongodb://localhost:27017"

SCHEMA_PATH="another_schema.json"

FLASK_ENV="development"

FLASK_APP="another_app.py"

FLASK_HOST="127.0.0.1"

FLASK_PORT="5555"

