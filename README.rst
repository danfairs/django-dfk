django-dfk
==========

django-dfk implements deferred foreign keys for Django. Deferred foreign keys are conceptually
similar to generic foreign keys, except that they are resolved to a real foreign key at runtime,
and cause proper foreign keys to be created in the database.

This package allows you to do two things::

    * Declare that a model's foreign key field is 'deferrable', and should be repointed later
    * Repoint an existing model's foreign key fields, even if that model is not django-dfk aware.

You should perform the latter with caution - consider it a similar process to monkey-patching!

This package is alpha software, and is not feature-complete. See the TODO section for what's
on the list.

django-dfk is compatible with Python 2.6, 2.7, 3.2 and 3.3.
django-dfk is compatible with django versions 1.3 - 1.5

Installation
============

Install ``django-dfk`` using your preferred Python package manager. Use of ``virtualenv`` is
also recommended::

    pip install django-dfk

Usage
=====

Pointing a single foreign key
-----------------------------

Let's say you want to reinvent the wheel, and develop a commenting app. Your comment model
might look like this, in ``mycomments.models``::

    from dfk import DeferredForeignKey

    class Comment(models.Model):
        commenter = models.ForeignKey('auth.User')
        content = DeferredForeignKey()
        body = models.TextField()


Now, you come to integrate this application with your blog system (which, as you're keen
on wheel reinvention, you have also written yourself). Here's ``blog/models.py``::

    from dfk import point
    from mycomments.models import Comment

    class BlogPost(models.Model):
        title = models.CharField(max_length=100)
        slug = models.SlugField()
        body = models.TextField()

    point(Comment, 'content', BlogPost)

The call to ``point`` will replace the ``DeferredForeignKey`` on ``Comment`` with a foreign key to BlogPost.

Pointing many foreign keys at once
----------------------------------

When writing models that use deferred foreign keys, you may need to declare that a number
should point to the same 'kind' of object. Let's say you had wild scope creep, and your
commenting app needed the ability to associate images with a blog post. So you edit
your comment app's models.py so it looks like this::

    from dfk import DeferredForeignKey

    class Comment(models.Model):
        commenter = models.ForeignKey('auth.User')
        content = DeferredForeignKey(name='Content')
        body = models.TextField()

    class Image(models.Model):
        image = models.ImageField()
        content = DeferredForeignKey(name='Content')

This expresses that both comments and images need to point to the same kind of model. This is
accomplished with the ``point_named`` function::

    from dfk import point_named
    point_named('blog', 'Content', BlogPost)

Now, all ``DeferredForeignKey`` instances in the ``blog`` app which are called ``Content`` will
be replaced by real foreign keys to ``BlogPost``.


Arguments to the generated foreign keys
---------------------------------------

When declaring a deferred foreign key, you may specify additional keyword arguments. Aside from
``name``, this will be passed on verbatim to the final foreign key.

It is also possible to pass arbitrary keyword arguments in calls to ``point`` or ``point_named``.
These will also be passed to the final foreign key. Where arguments are present in both the
DFK definition and in the ``point``/``point_named`` call, arguments from the latter will take
precedence.

Model inheritance
-----------------

Model inheritance should Just Work. It's possible to have ``DeferredForeignKey``
instances on subclasses and base classes. The only thing to be aware of is that
repointing a dfk on a subclass where the key is actually defined on a
non-abstract base class is illegal, and will raise a ``TypeError``.

Cleaning object caches
----------------------

Pointing or repointing foreign keys requires that related object caches are
repopulated as relationships will have changed and things like filtering on
related objects are likely to fail.

By default object caches are cleaned after each ``point`` or ``repoint``.
For apps with many ``DeferredForeignKey`` instances involving the same model
it may be more efficient to clean the caches once, after all pointing and
repointing has finished. To enable this pass ``clean_caches=False`` to
``point`` or ``repoint`` and then manually call ``clean_object_caches`` as
required::

    from dfk import point
    from dfk import clean_object_caches
    from mycomments.models import Comment

    class BlogPost(models.Model):
        title = models.CharField(max_length=100)
        slug = models.SlugField()
        body = models.TextField()

    point(Comment, 'content', BlogPost, clean_caches=False)
    clean_object_caches(Comment, BlogPost)


Acknowledgements
================

Thanks to ISM Fantasy Games Ltd. for sponsoring this package.
Package maintained by Dan Fairs and Rob Charlwood
