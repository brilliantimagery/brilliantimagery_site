# Brilliant Imagery Site

## Development

### Instillation

If you don't already have `pipenv` installed, instalal it. Note: it can't be installed into a virtual environment.

```
$ pip install pipenv
```

Create a virtual environment and install both the dev and production dependencies. This need's to be done from within the top level `bi_site` folder, the folder in which the `Pipfile` file is located.

```
$ pipenv install --dev
```

### Dev Server Initialization and Setup

A `config.py` file needs to be generated. This can be done by duplicating the file `\bi_site\config_example.py` and rename it to generate the file `\bi_site\config.py`. Change the enclosed string values as needed. `SECRET_KEY` is a 50 character random string. `EMAIL_HOST_USER` is the email address that the site will sends things such as password change emails from. The present settings file assumes that it's an email address managed by GMail. `EMAIL_HOST_PASSWORD` is the password for the entered email. The system also assumes that 2FA has been set up for the email address and that the password is the password generated for an app. Setting up 2FA and getting the app password is beyond the scop of this README.

Create database migration files:

```
$ python manage.py makemigrations
```

Create the database and tables:

```
$ python manage.py migrate
```

Create a superuser to manage the site:

```
$ python manage.py createsuperuser
```

### Running the Dev Server

Start the virtual environment if it isn't already running:

```
$ pipenv shell
```

Start the test server:

```
$ python manage.py runserver
```

### Testing

Start the virtual environment if it isn't yet running. This need's to be done from within the top level `bi_site` folder.

```
$ pipenv shell
```

To run all tests:

```
$ pytest
```

If test coverage is to be generated insure that no lines in `pytest.ini` are commented out.

```ini
[pytest]
DJANGO_SETTINGS_MODULE = bi_site.settings
addopts = --cov --cov-report=html
```

Coverage generation can cause issues with IDE debuggers that result in breakpoints not being honored. If an IDE isn't stopping at your breakpoints, comment out the `addopts` line from `pytest.ini`.

```ini
[pytest]
DJANGO_SETTINGS_MODULE = bi_site.settings
;addopts = --cov --cov-report=html
```
