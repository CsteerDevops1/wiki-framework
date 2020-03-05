
## coreSerice

Mongodb uses ./data/db folder for it's backups and etc.
Database and API validation are automatically set from schema.json file.

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

Use start.sh script to launch everything
