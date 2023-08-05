# -*- coding: utf-8 -*-
from djangoplus import cache
from djangoplus.utils.metadata import set_metadata, iterable


def meta(verbose_name, can_view=(), formatter=None, dashboard=None):
    def decorate(func):
        set_metadata(func, 'type', 'attr')
        set_metadata(func, 'verbose_name', verbose_name)
        set_metadata(func, 'can_view', can_view)
        set_metadata(func, 'formatter', formatter)
        set_metadata(func, 'position', dashboard)
        return func
    return decorate


def subset(title, can_view=(), alert=False, notify=None, menu=None, sequence=0):
    def decorate(function):
        set_metadata(function, 'type', 'subset')
        set_metadata(function, 'tab', True)
        set_metadata(function, 'title', title)
        set_metadata(function, 'alert', alert)
        set_metadata(function, 'notify', notify)
        set_metadata(function, 'menu', menu)
        set_metadata(function, 'sequence', sequence)
        set_metadata(function, 'can_view', iterable(can_view))
        set_metadata(function, 'name', function.func_name)
        set_metadata(function, 'order', cache.next_number())
        return function

    return decorate


def action(title, can_execute=(), condition=None, category=u'Ações', style='popup', input=None,
           message=u'Ação realizada com sucesso.', initial=None, choices=None, inline=None, icon=None,
           sequence=0, can_execute_by_organization=None, can_execute_by_unit=None, can_execute_by_role=None, redirect_to=None, menu=None):
    def decorate(function):
        function._action = dict(
            title=title, can_execute=iterable(can_execute),
            input=input, group=category or title, css=style, condition=condition, view_name=function.__name__,
            message=message, initial=initial or '%s_initial' % function.__name__, function=function,
            choices=choices or '%s_choices' % function.__name__, inline=inline, icon=icon, doc=function.__doc__,
            sequence=sequence, can_execute_by_organization=iterable(can_execute_by_organization),
            can_execute_by_unit=iterable(can_execute_by_unit), can_execute_by_role=iterable(can_execute_by_role),
            redirect_to=redirect_to, menu=menu
        )
        return function

    return decorate