from django.db.models import ForeignKey
from dfk.models import DeferredForeignKey

def point(from_model, rel_name, to_model):
    deferred_fk = getattr(from_model, rel_name)
    if not isinstance(deferred_fk, DeferredForeignKey):
        raise ValueError, u'You only point a DeferredForegnKey'
    
    target_model = '%s.%s' % (
        to_model._meta.app_label,
        to_model._meta.object_name
    )
    new_foreign_key = ForeignKey(
        target_model, 
        *deferred_fk.args, 
        **deferred_fk.kwargs
    )
    from_model.add_to_class(rel_name, new_foreign_key)
    
def repoint(from_model, rel_name, to_model, **kwargs):
    options = getattr(to_model, '_meta', None)
    if options:
        assert not options.abstract, u'Target model may not be abstract'
    field = from_model._meta.get_field(rel_name)
    rel = field.rel
    args = (to_model, rel.field_name)
    new_kwargs = {
        'related_name': rel.related_name,
        'limit_choices_to': rel.limit_choices_to,
        'lookup_overrides': rel.lookup_overrides,
        'parent_link': rel.parent_link
    }
    new_kwargs.update(kwargs)
    new_rel = rel.__class__(*args, **new_kwargs)
    field.rel = new_rel
