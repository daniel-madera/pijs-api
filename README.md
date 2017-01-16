# pijs-api
API for PIJS - Personal vocabulary for elementary school students

## Install requirements
sudo apt-get install python3.5-dev python3-psycopg2 python3-pip
sudo pip3 install --upgrade pip
sudo pip3 install virtualenv
virtualenv env -p python3.5
source env/bin/activate
pip install -r requirements.pip


## DB install requirements
sudo apt-get install postgresql-9.5 postgresql-client  postgresql-client-common postgresql-common

sudo -u postgres psql
postgres=# alter user postgres password 'postgres';
sudo vim /etc/postgresql/9.5/main/pg_hba.conf // edit peer to md5
createuser -U postgres -d -e -E -l -P -r -s pijs
createdb -U pijs pijs_api

python manage.py migrate
python manage.py test api
python manage.py loaddata app-startup
python manage.py loaddata test-data // for testing

