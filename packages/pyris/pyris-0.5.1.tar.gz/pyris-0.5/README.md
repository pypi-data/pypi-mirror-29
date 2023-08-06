# Pyris

IRIS INSEE Geolocalizer

Pyris try to collect data about
[IRIS](http://www.insee.fr/fr/methodes/default.asp?page=zonages/iris.htm) from
the French [INSEE](http://www.insee.fr/en/) institute. It's possible from an
address to find the IRIS code and some related data.

[IRIS](http://www.insee.fr/fr/methodes/default.asp?page=zonages/iris.htm) are
specific codes and data related to more than 50,000 districts, built by the
[National Institute of Statistics and Economic Studies](http://www.insee.fr/en/).

* Running instance http://pyris.datajazz.io/
* API documentation at http://pyris.datajazz.io/doc/

## Interactive Map

![map](./images/pyris-map.jpg)

## REST API documentation

![api](./images/pyris-doc-api.png)

For instance, you can:

* `URL/iris/0104?limit=5` to the some information about a specific IRIS code

* `URL/search/q=place de la bourse Bordeaux` to get the IRIS data from a
  specific address

## Data

IRIS shapes at https://www.data.gouv.fr/fr/datasets/contour-des-iris-insee-tout-en-un/

Go to the `data` directory and then:

* `./01-download-data.sh`

You have to install postgreSQL and PostGIS. For Debian:

    sudo apt-get install postgresql postgis

Create a database name `pyris` with:

* `02-create-database.sh`
* and `03-insert-data.sh` to insert data

You have to be a PostgreSQL superuser to create the postgis extension for your
database. If it's not the case, you can do:

* `su`
* `su - postgres`
* `psql pyris -c "CREATE EXTENSION postgis;"`

Test the insertion with a simple:

```sql
SELECT gid,depcom,nom_com,iris,typ_iris
FROM geoiris LIMIT 10;
```

## Launch the Web App

First, download the few CSS & JavaScript dependencies with a `bower install`
(just a Bootstrap and jQuery).

Then :
`> gunicorn -b 127.0.0.1:5555 pyris.api.run:app`
or
`> gunicorn -b 127.0.0.1:5555 --env PYRIS_APP_SETTINGS=./appdev.yml pyris.api.run:app`
if you have to specify db credentials or logging Flask app configuration.

See an [example of a app.yml file](https://github.com/garaud/pyris/blob/master/app.yml)

Visit http://localhost:5555/pyris

## Requirements

* postgresql
* postgis

* flask
* flask restplus
* psycopg2
* slumber
* pyaml
