from __future__ import unicode_literals
from django.db.models import ForeignKey
from django.db.models.loading import get_app
from django.db.models.loading import get_models
from dfk.models import DeferredForeignKey

_marker = object()

try:
    unicode = unicode
except NameError:
    unicode = str
    basestring = (str, bytes)


def point(from_model, rel_name, to_model, clean_caches=True, **fk_kwargs):
    """
    Cause the foreign key `rel_name` on `from_model` to point to
    `to_model`. clean_caches can be set to False if you plan to handle the
    cleaning of object caches yourself. `fk_kwargs` will be forwarded to the
    generated foreign key.
    """
    assert not to_model._meta.abstract
    deferred_fk = getattr(from_model, rel_name)
    if not isinstance(deferred_fk, DeferredForeignKey):
        raise ValueError('You only point a DeferredForeignKey')

    # Need to check if this deferred fk is defined in a non-abstract
    # base class
    for parent in from_model._meta.parents:
        # Abstract parent, that's OK
        if not parent._meta.abstract and \
                getattr(parent, rel_name, _marker) is not _marker:
            raise TypeError('You may not repoint subclass '
                            'fields defined on a non-abstract base '
                            'class')

    target_model = '%s.%s' % (
        to_model._meta.app_label,
        to_model._meta.object_name
    )

    new_kwargs = deferred_fk.kwargs.copy()
    new_kwargs.update(fk_kwargs)
    new_foreign_key = ForeignKey(
        target_model,
        *deferred_fk.args,
        **new_kwargs
    )
    from_model.add_to_class(rel_name, new_foreign_key)

    # Need to repopulate related name caches on both Meta classes.
    if clean_caches:
        clean_object_caches(from_model, new_foreign_key.rel.to)


def point_named(app_name, target_name, to_model, **fk_kwargs):
    # Grab all the models from the app
    if isinstance(app_name, basestring):
        app = get_app(app_name)
    else:
        app = app_name
    models = get_models(app, include_deferred=True)

    # Now look for dfk instances with the target name
    for model in models:
        for attr in dir(model):
            # Fields using models.SubfieldBase object to being got - but we
            # can skip those anyway.
            ob = getattr(model, attr, None)
            if not isinstance(ob, DeferredForeignKey):
                continue

            # We found a deferred foreign key. Check the name
            # to see if it's the one we're processing.
            if getattr(ob, 'name', None) != target_name:
                continue

            # We found a foreign key. Repoint it.
            point(model, attr, to_model, **fk_kwargs)


def repoint(from_model, rel_name, to_model, clean_caches=True, **kwargs):
    options = getattr(to_model, '_meta', None)
    if options:
        assert not options.abstract, 'Target model may not be abstract'
    field = from_model._meta.get_field(rel_name)
    rel = field.rel

    # Does our relationship class quack like a Django 1.6+ ForeignObject
    if hasattr(rel.__class__, 'get_joining_columns'):
        args = (field, to_model, rel.field_name)
    else:
        args = (to_model, rel.field_name)

    new_kwargs = {
        'related_name': rel.related_name,
        'limit_choices_to': rel.limit_choices_to,
        'parent_link': rel.parent_link
    }

    # Pre-1.3
    if hasattr(rel, 'lookup_overrides'):
        new_kwargs['lookup_overrides'] = rel.lookup_overrides
    # 1.3
    if hasattr(rel, 'on_delete'):
        new_kwargs['on_delete'] = rel.on_delete

    new_kwargs.update(kwargs)
    new_rel = rel.__class__(*args, **new_kwargs)
    field.rel = new_rel
    if clean_caches:
        clean_object_caches(from_model, to_model)


def clean_object_caches(*models):
    # Repopulate related object caches when a point or repoint is done, as
    # relationships will have changed. Without this, things like filtering
    # on related objects is likely to fail.
    for model in models:
        model._meta._fill_related_objects_cache()
        model._meta.init_name_map()
