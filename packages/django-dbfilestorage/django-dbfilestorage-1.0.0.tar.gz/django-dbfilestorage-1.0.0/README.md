# Django-dbfilestorage

[![CircleCI](https://circleci.com/gh/tyrelsouza/django-dbfilestorage.svg?style=svg)](https://circleci.com/gh/tyrelsouza/django-dbfilestorage) [![codecov](https://codecov.io/gh/tyrelsouza/django-dbfilestorage/branch/master/graph/badge.svg)](https://codecov.io/gh/tyrelsouza/django-dbfilestorage)

Custom file storage for Django that stores file data and content type in the database.
Easy to use for testing remote storages when you're in a transition stage between Local and something like Amazon S3.

Intended to be used in tests, never in production.

## TESTING

I use Pyenv and Tox to support Python2.7.13 and Python3.6.3

```
pip install -r requirements-dev.txt
pyenv install 2.7.13 3.5.4 3.6.3
tox
```

Or you can run individually with your shell python using `python setup.py test`

## INSTALLATION

```
pip install django-dbfilestorage
```

Then in your project's `settings.py` file, add `'dbfilestorage'` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = (
    ...
    'dbfilestorage'
)
```

Next, if you want to set this globally, set the setting:

```python
DEFAULT_FILE_STORAGE='dbfilestorage.storage.DBFileStorage'
```

Or you can set it individually on a field: [Django Docs](https://docs.djangoproject.com/en/1.10/ref/models/fields/#django.db.models.FileField.storage)

```python
from dbfilestorage.storage import DBFileStorage

class SomeClass(models.Model):
    file = models.FileField(upload_to=u'anywhere',
        storage=DBFileStorage())
```


## TODO

- Test that this works on a fake model, not just the storage file.
- Different django versions.

## Signing Key
You can find my signing key at [TyrelSouza.com](https://tyrelsouza.com/koken/?/pages/pgp-keys/)

I will sign everything with 0x769A1BC78A2DDEE2

## CHANGELOG

- 2018-03-01 [Tyrel Souza] Release Version 1.0.0
- 2018-02-01 [Tyrel Souza] Bump versions to django 1.11 and testing with Python3
- 2017-05-10 [Pamela McA'Nulty] Have save overwrite existing files
- 2017-02-06 [Tyrel Souza] Set primary key to `id` not `name`, this involves a lot of migrations, so I've kept them in multiple files
- 2017-01-27 [Tyrel Souza] Get rid of filehash
- 2017-01-26 [Tyrel Souza] Check filehash and filename, not just hash when checking if it needs to be saved.
- 2017-01-25 [Tyrel Souza] Keeping Filename on upload.
- 2017-01-23 [Tyrel Souza] Add Modified Time to storage support
- 2017-01-23 [Tyrel Souza] Everything should return a "filename" even if it's generated. Make the filename be the hash + ext. (fall back to .txt)
- 2017-01-20 [Tyrel Souza] Make path return None if no file
- 2017-01-20 [Tyrel Souza] Make path return filename
- 2017-01-20 [Tyrel Souza] Add another migration, and redo all the initial migrations.
- 2017-01-20 [Tyrel Souza] Make sure migrations is actually there.
- 2017-01-20 [Tyrel Souza] Split filename and filehash.
- 2016-12-09 [Tyrel Souza] Add signing key to readme.
- 2016-12-09 [Tyrel Souza] Update Tests, add some cleanup.
- 2016-12-08 [Tyrel Souza] Add more documentation.
- 2016-12-07 [Tyrel Souza] Update Readme, move to github, gitlab wasn't functioning properly.
- 2016-12-07 [Tyrel Souza] Initial commits and basic project setup
