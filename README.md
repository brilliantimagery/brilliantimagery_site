# Brilliant Imagery Site

## Instillation

## Testing

to install all test and production dependencies:

```
$ pipenv install -dev
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
