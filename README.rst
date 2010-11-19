django-dfk
==========

django-dfk implements deferred foreign keys for Django. This package allows
you to do two things::

    * Declare that a model's foreign key field is 'deferrable', and should be repointed later
    * Repoint an existing model's foreign key fields, even if that model is not django-dfk aware.

You should perform the latter with caution - consider it a similar process to monkey-patching!


