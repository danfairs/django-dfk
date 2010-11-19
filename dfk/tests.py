from django.db import models
from django.test import TestCase

from dfk import point
from dfk import point_named
from dfk import repoint
from dfk.models import DeferredForeignKey

class ModelA(models.Model):
    pass

class ModelB(models.Model):
    fk = models.ForeignKey(ModelA)

class ModelC(models.Model):
    pass

class NotAModel(object):
    pass

class AbstractModel(models.Model):
    class Meta:
        abstract = True

# Repoint ModelB's foreign key field 'fk' to ModelC
repoint(ModelB, 'fk', ModelC)

class ExistingTestCase(TestCase):

    def test_existing_fk(self):
        # We've repointed ModelB's 'fk' field to reference
        # ModelC, rather than ModelA. Check this has worked
        # as expected
        c = ModelC.objects.create()
        b = ModelB.objects.create(fk=c)
        b.save()

        x = ModelB.objects.get(pk=b.pk)
        self.assertEqual(c, b.fk)

    def test_not_a_model(self):
        self.assertRaises(AssertionError, repoint, ModelB, 'fk', NotAModel)

    def test_abstract(self):
        self.assertRaises(AssertionError, repoint, ModelB, 'fk', AbstractModel)


class DeferredModelA(models.Model):
    user = DeferredForeignKey()

class DeferredModelB(models.Model):
    content = DeferredForeignKey(name='content_reference')

class DeferredModelC(models.Model):
    content = DeferredForeignKey(name='content_reference')

# Point DeferredModelA's 'user' dfk to ModelA
point(DeferredModelA, 'user', ModelA)

# Point DeferredForeignKey of class 'content_reference' to ModelB,
# only in the dfk app
point_named('content_reference', ModelC, 'dfk')

class DeferredForeignKeyTestCase(TestCase):

    def test_specific_field(self):
        # Check that DeferredModelA's deferred field was correctly
        # processed
        m = ModelA.objects.create()
        a = DeferredModelA.objects.create(
            user=m
        )
        x = DeferredModelA.objects.get(pk=a.pk)
        self.assertEqual(m, x)

    def test_class(self):
        # Check that processing a whole class of deferred fields
        # works as expected
        t = ModelC.objects.create()
        b = DeferredModelB.objects.create(content=t)
        c = DeferredModelC.objects.create(content=t)

        self.assertEqual(t, DeferredModelB.objects.get(pk=b.pk).content)
        self.assertEqual(t, DeferredModelC.objects.get(pk=c.pk).content)

    def test_duplicate(self):
        # Attempting to point a dfk to a different target once
        # it's already been set should raise an error
        self.assertRaises(ValueError, point, DeferredModelA, 'user', ModelC)
