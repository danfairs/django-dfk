from django.db import models
from django.test import TestCase

from dfk import point
from dfk import point_named
from dfk import repoint
from dfk.models import DeferredForeignKey

class CustomField(models.CharField):
    __metaclass__ = models.SubfieldBase

class ModelA(models.Model):
    pass

class ModelB(models.Model):
    fk = models.ForeignKey(ModelA)

class ModelC(models.Model):
    pass

class ModelD(models.Model):
    fk = DeferredForeignKey(name='content')

class ModelCustomField(models.Model):
    fk = DeferredForeignKey(name='content2')
    other = CustomField(max_length=10)

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
    user = DeferredForeignKey()

# Point DeferredModelA's 'user' dfk to ModelA
point(DeferredModelA, 'user', ModelA, related_name='foo_set')

# Point ModelD's deferred fk to ModelA
point_named('dfk', 'content', ModelA)

# Point ModelCustomFiekld's deferred fk to ModelA
point_named('dfk', 'content2', ModelA)

class DeferredForeignKeyTestCase(TestCase):

    def test_specific_field(self):
        # Check that DeferredModelA's deferred field was correctly
        # processed
        m = ModelA.objects.create()
        a = DeferredModelA.objects.create(
            user=m
        )
        x = DeferredModelA.objects.get(pk=a.pk).user
        self.assertEqual(m, x)

        # Also test that the related_name override was passed
        # through
        self.assertEqual(1, len(x.foo_set.all()))

    def test_duplicate(self):
        # Attempting to point a dfk to a different target once
        # it's already been set should raise an error
        self.assertRaises(ValueError, point, DeferredModelA, 'user', ModelC)

    def test_point_non_deferred(self):
        # Attempting to point a non-DeferredForeignKey should raise a
        # ValueError
        self.assertRaises(ValueError, point, ModelB, 'fk', ModelC)

    def test_point_abstract(self):
        # Attempting to point a dfk to an abstract class should raise
        # a AssertionError
        self.assertRaises(AssertionError, point, DeferredModelB, 'user', AbstractModel)

    def test_named_deferred(self):
        # Check that our repoint of the named foreign key worked
        a = ModelA.objects.create()
        d = ModelD.objects.create(fk=a)
        self.assertEqual(a, ModelD.objects.get(pk=d.pk).fk)

    def test_class_using_custom_fields_with_subfield_base(self):
        # Check that we our repoint of the named fk on the model with a
        # custom field worked
        a = ModelA.objects.create()
        d = ModelCustomField.objects.create(fk=a, other='hi')
        self.assertEqual(a, ModelCustomField.objects.get(pk=d.pk).fk)

