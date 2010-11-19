def point(from_model, rel_name, to_model):
    pass
    
def point_named(name, to_model, app_label):
    pass

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
