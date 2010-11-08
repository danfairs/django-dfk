from django.db import models
from django.test import TestCase

from dfk import repoint

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
    
repoint(ModelB, 'fk', ModelC)
    
class ExistingTestCase(TestCase):
    
    def test_existing_fk(self):
        c = ModelC.objects.create()
        b = ModelB.objects.create(fk=c)
        b.save()
        
        x = ModelB.objects.get(pk=b.pk)
        self.assertEqual(c, b.fk)
        
    def test_not_a_model(self):
        self.assertRaises(ValueError, repoint, ModelB, 'fk', NotAModel)

    def test_abstract(self):
        self.assertRaises(ValueError, repoint, ModelB, 'fk', AbstractModel)