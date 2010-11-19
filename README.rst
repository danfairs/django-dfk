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

Pointing may foreign keys at once
---------------------------------

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

Acknowledgements
================

Thanks to ISM Fantasy Games Ltd. for sponsoring this package.
