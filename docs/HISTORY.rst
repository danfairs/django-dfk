0.0.10
=====
- Setup Tox environments for Django 1.7
- Added MIDDLEWARE_CLASSES definition to test settings to avoid warnings from
  Django 1.7's system check.
- Added install_requires limits to setup.py to reflect supported versions of
  Django
- Updated docs.

0.0.9
=====
- Setup Tox environments for Django 1.6
- Fixed repoint issues under Django 1.6 due to use of new ForeignObject baseclass for related objects.  


0.0.8
=====
- Make codebase Python 3 compatible (3.2, 3.3) (robcharlwood@gmail.com).
- Make codebase compatible with django 1.5.4 (robcharlwood@gmail.com)
- New Python 3 compatible codebase has been tested against django 1.5.4 (robcharlwood@gmail.com)
- Carried out full tidy up with PEP8 compliance. (robcharlwood@gmail.com)
- Setup and configured ``django-dfk`` for use with ``tox`` testing library (robcharlwood@gmail.com)
- Added full documentation on running test suite (robcharlwood@gmail.com)

0.0.7
=====

Make cache cleaning optional, and fix some PEP8 compliance issues. Thanks
to Mark Hughes (mark@ismgames.com).

0.0.6
=====

Fix a problem where repointing a deferred foreign key defined on a non-abstract
base class through a subclass would result in a new field being added to the
local_fields of the subclass, shadowing the one on the base class. It is now
illegal to do this; dfks on base classes should be pointed using the base class
itself.

0.0.5
=====

Fix a problem where related object caches on models' _meta Options classes
were not being repopulated on a repoint. This led to problems where
filtering on a parent model related to a child using a deferred foreign key
could fail if the dfk was (re)pointed after the initial phase of model loading
had already taken place.

0.0.4
=====

- Include a MANIFEST.in to ensure docs are packaged.

0.0.3
=====
- Fix packaging error

0.0.2
=====

- Fix an issue when repointing foreign keys on model classes with custom
  fields which use the django.db.models.SubfieldBase metaclass
- Fix an issue migrating from Django 1.2 to 1.3.

0.0.1
=====

- Initial version
