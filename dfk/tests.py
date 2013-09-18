from __future__ import unicode_literals
from django.db import models
from django.test import TestCase

from dfk import point
from dfk import point_named
from dfk import repoint
from dfk import clean_object_caches
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
        self.assertRaises(
            AssertionError, point, DeferredModelB, 'user', AbstractModel)

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

    def test_options_caches_cleared_on_point(self):
        # Check that the relevant meta caches are cleared after a point
        # to ensure related field names are up to date.
        class NewModel(models.Model):
            c = DeferredForeignKey()

        point(NewModel, 'c', ModelC)
        mdc_related = ModelC._meta.get_all_related_objects_with_model()
        found = False
        for rel, _ in mdc_related:
            if rel.model is NewModel:
                found = True
        self.assertEqual(True, found)

    def test_options_caches_not_cleared_on_point(self):
        # Check that the relevant meta caches are not cleared after a point
        # if clear_caches=False
        class NewModelNoCache(models.Model):
            c = DeferredForeignKey()

        point(NewModelNoCache, 'c', ModelC, clean_caches=False)
        mdc_related = ModelC._meta.get_all_related_objects_with_model()
        found = False
        for rel, _ in mdc_related:
            if rel.model is NewModelNoCache:
                found = True
        self.assertEqual(False, found)

    def test_options_caches_cleaned(self):
        # Check that the relevant meta caches are cleared after
        # a direct call to clean_object_caches
        class NewModelNoCache2(models.Model):
            c = DeferredForeignKey()

        point(NewModelNoCache2, 'c', ModelC, clean_caches=False)
        mdc_related = ModelC._meta.get_all_related_objects_with_model()
        found = False
        for rel, _ in mdc_related:
            if rel.model is NewModelNoCache2:
                found = True
        assert not found

        clean_object_caches(NewModelNoCache2, ModelC)
        mdc_related = ModelC._meta.get_all_related_objects_with_model()
        for rel, _ in mdc_related:
            if rel.model is NewModelNoCache2:
                found = True
        self.assertEqual(True, found)

    def test_options_caches_cleared_on_repoint(self):
        # Check that the relevant meta caches are cleared after a repoint
        # to ensure related field names are up to date.
        class NewModel2(models.Model):
            c = DeferredForeignKey()

        point(NewModel2, 'c', ModelA)
        repoint(NewModel2, 'c', ModelC)
        mdc_related = ModelC._meta.get_all_related_objects_with_model()
        found = False
        for rel, _ in mdc_related:
            if rel.model is NewModel2:
                found = True
        self.assertEqual(True, found)

    def test_options_caches_not_cleared_on_repoint(self):
        # Check that the relevant meta caches are not cleared after a repoint
        # if clear_caches=False
        class NewModel2NoCache(models.Model):
            c = DeferredForeignKey()

        point(NewModel2NoCache, 'c', ModelA)
        repoint(NewModel2NoCache, 'c', ModelC, clean_caches=False)
        mdc_related = ModelC._meta.get_all_related_objects_with_model()
        found = False
        for rel, _ in mdc_related:
            if rel.model is NewModel2NoCache:
                found = True
        self.assertEqual(False, found)

    def test_derived_model(self):
        # If we point a field on a derived model that actually is
        # defined on the base class, then we should get a TypeError
        class BaseClass1(models.Model):
            c = DeferredForeignKey()

        class DerivedModel1(BaseClass1):
            pass
        self.assertRaises(TypeError, point, DerivedModel1, 'c', ModelA)

    def test_derived_model_abstract(self):
        # If the base model is abstract, then it's actually OK as
        # the field is local to the subclass anyway.
        class BaseClass2(models.Model):
            c = DeferredForeignKey()

            class Meta:
                abstract = True

        class DerivedModel2(BaseClass2):
            pass
        point(DerivedModel2, 'c', ModelA)
        self.assertEqual(ModelA, DerivedModel2.c.field.rel.to)

    def test_derived_model_point_base(self):
        # If we repoint a dfk on a base non-abstract class, subclasses
        # should see the change.
        class BaseClass3(models.Model):
            c = DeferredForeignKey()

        class DerivedModel3(BaseClass3):
            pass
        point(BaseClass3, 'c', ModelA)
        self.assertEqual(ModelA, DerivedModel3.c.field.rel.to)
