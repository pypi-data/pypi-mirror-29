# -*- coding: utf-8 -*-
from django.apps import apps
from django.contrib.auth.models import Permission, Group, ContentType
from django.db.models import signals
from django.contrib.auth.management import create_permissions
from djangoplus.utils.metadata import get_metadata
from djangoplus.cache import loader


def sync_permissions():

    default_permissions_names = dict(edit='Editar', add='Cadastrar', delete=u'Excluir', list='Listar')

    # Permission.objects.all().delete()
    # Group.objects.all().delete()

    for group in Group.objects.all():
        group.permissions.clear()

    for Model in apps.get_models():
        model_name = Model.__name__.lower()
        app_label = Model._meta.app_label

        if '_' not in model_name and not (model_name == 'user' and app_label == 'auth'):

            model = Model.__name__.lower()

            qs_content_type = ContentType.objects.filter(app_label=app_label, model=model)
            if qs_content_type.exists():
                content_type = qs_content_type[0]
            else:
                content_type = ContentType.objects.create(app_label=app_label, model=model)

            for codename, name in default_permissions_names.items():
                codename = '%s_%s' % (codename, content_type.model)
                name = '%s %s' % (name, Model._meta.verbose_name)
                qs_permission = Permission.objects.filter(codename=codename, content_type=content_type)
                if qs_permission.exists():
                    qs_permission.update(name=name)
                else:
                    Permission.objects.create(codename=codename, name=name, content_type=content_type)
            permissions = []
            admin_groups = []
            for admin_group in get_metadata(Model, 'can_admin', (), iterable=True):
                admin_groups.append(admin_group)
            for scope in ('role', 'unit', 'organization'):
                for admin_group in get_metadata(Model, 'can_admin_by_%s' % scope, (), iterable=True):
                    admin_groups.append(admin_group)
            admin_groups = tuple(admin_groups)

            relate_groups = get_metadata(Model, 'can_relate', (), iterable=True)

            for codename, name, groups in get_metadata(Model, 'permissions', []):
                qs_permission = Permission.objects.filter(codename=codename, content_type=content_type)
                if qs_permission.exists():
                    qs_permission.update(name=name)
                else:
                    Permission.objects.create(codename=codename, name=name, content_type=content_type)
                if groups or admin_groups or relate_groups:
                    permissions.append((codename, admin_groups + groups + relate_groups))

            for codename in default_permissions_names:
                attr_name = 'can_%s' % codename
                groups = []
                for group in get_metadata(Model, attr_name, (), iterable=True):
                    groups.append(group)
                for scope in ('role', 'unit', 'organization'):
                    for group in get_metadata(Model, '%s_by_%s' % (attr_name, scope), (), iterable=True):
                        groups.append(group)
                groups = tuple(groups)
                if groups or admin_groups:
                    permissions.append((codename, admin_groups + groups))
                if relate_groups and codename != 'list':
                    permissions.append((codename, relate_groups))

            for codename, group_names in permissions:

                if codename in default_permissions_names:
                    codename = '%s_%s' % (codename, model)

                permission = Permission.objects.get(codename=codename)
                for group_name in group_names:
                    group_name = hasattr(group_name, '_meta') and group_name._meta.verbose_name or group_name

                    if group_name in loader.abstract_role_model_names:
                        for concrete_group_name in loader.abstract_role_model_names[group_name]:
                            group = Group.objects.get_or_create(name=concrete_group_name.strip())[0]
                            group.permissions.add(permission)
                    else:
                        group = Group.objects.get_or_create(name=group_name.strip())[0]
                        group.permissions.add(permission)

    for view in loader.views:
        function = view.get('function')
        if function:
            name = view.get('title')
            can_view = view.get('can_view', ())
            if can_view:
                content_type = ContentType.objects.get(app_label='admin', model='user')
                qs_permission = Permission.objects.filter(codename=function.func_name, content_type=content_type)
                if qs_permission.exists():
                    qs_permission.update(name=name)
                    permission = qs_permission[0]
                else:
                    permission = Permission.objects.create(codename=function.func_name, content_type=content_type, name=name)
                for group in Group.objects.filter(name__in=can_view):
                    group.permissions.add(permission)

    for actions_dict in (loader.actions, loader.class_actions):
        for model in actions_dict:
            app_label = get_metadata(model, 'app_label')
            content_type = ContentType.objects.get(app_label=app_label, model=model.__name__.lower())
            for category in actions_dict[model]:
                for key in actions_dict[model][category].keys():
                    name = actions_dict[model][category][key]['title']
                    can_execute = []
                    for scope in ('', 'role', 'unit', 'organization'):
                        scope = scope and '_by_%s' % scope or scope
                        for group_name in actions_dict[model][category][key].get('can_execute%s' % scope) or ():
                            can_execute.append(group_name)
                    if can_execute:
                        qs_permission = Permission.objects.filter(codename=key, content_type=content_type)
                        if qs_permission.exists():
                            qs_permission.update(name=name)
                            permission = qs_permission[0]
                        else:
                            permission = Permission.objects.get_or_create(codename=key, content_type=content_type, name=name)[0]
                        for group in Group.objects.filter(name__in=can_execute):
                            group.permissions.add(permission)

signals.post_migrate.disconnect(create_permissions, dispatch_uid="django.contrib.auth.management.create_permissions")
