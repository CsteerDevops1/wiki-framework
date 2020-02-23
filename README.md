# wiki-framework

## Rules

All work, including comments on tickets, comments in the code are in English.

Spelling or grammar errors are "bugs" and must be "fixed." 

Data in the project can be in any languages. 

User interaction - through localization packages, default value = en US, but from the very beginning I would like to see ru RU available.

Use gitignore file.
  
  
  ## Process
  
The master branch contains the official release history, and the develop branch serves as an integration branch for new features.
We do large features in our branches.
Then we do a pull request and someone watches the performance.


## Project

The current status of the project can be viewed in "Projects" > "Framework". There are todo columns, solved task column. Add tasks to these columns.
Write current errors and problems in isseus.


## coreSerice

The coreService/data/db folder must be created with correct (a+rw ?) mode bits set on it.
Use docker-compose up --build to start core service on port 5000

API documentation is on /api/wiki/doc


## Description of the project

Fillable database in wiki format. The database fill interface is the telegram bot. The database populating interface is a telegram bot. Minimum functionality: add material, edit property, add photo, sound file, video clip. Display materials on the web site in the form of “MarkDown” or in another format. 

Technologies: python3.7, telegram API, flask, nginx, wsgi, MongoDB.

Simple scheme of project https://miro.com/app/board/o9J_kwo6HM0=/
