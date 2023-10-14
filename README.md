# Rysgally Project

rysgally-project is a mini project management software (like Microsoft Project)

# Features

- v0.1 - manage employees' commits
- v1.1 - rating technology (commit bonus)

# Installation

````
git clone https://github.com/Hojagulyyev/rysgally-project.git

cd rysgally-project

virtualenv venv

. source/bin/activate

pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
````