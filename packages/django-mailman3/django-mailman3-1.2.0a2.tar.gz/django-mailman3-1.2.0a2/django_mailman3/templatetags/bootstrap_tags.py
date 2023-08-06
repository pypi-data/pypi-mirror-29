# -*- coding: utf-8 -*-
# Copyright (C) 2012-2018 by the Free Software Foundation, Inc.
#
# This file is part of Postorius.
#
# Postorius is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# Postorius is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# Postorius.  If not, see <http://www.gnu.org/licenses/>.

from django import template
try:
    from django.forms.boundfield import BoundField
except ImportError:
    # For Django <=1.9
    from django.forms.forms import BoundField             # pragma: nocover

register = template.Library()


@register.filter(name='add_form_control')
def add_form_control(field):
    return field.as_widget(attrs={'class': 'form-control'})


@register.filter('fieldtype')
def fieldtype(field):
    """
    Return the name of the field's class.

    :name field: Field should a given field.
    :type field: django.forms.boundfield.BoundField
    """
    assert isinstance(field, BoundField)
    return field.field.widget.__class__.__name__


@register.filter('fieldtype_is')
def fieldtype_is(field, widget_class):
    """
    Given a field and a widget class, check if the field is a subclass of the
    widget class.

    :name field: Field should a given field.
    :type field: django.forms.boundfield.BoundField
    :name widget_class: Django form widget class.
    :type widget_class: django.forms.widgets.Widget
    """
    assert isinstance(field, BoundField)
    return widget_class in [
        parent.__name__ for parent in
        field.field.widget.__class__.__mro__]


@register.filter('is_checkbox')
def is_checkbox(field):
    """
    Given the field, check if it is a checkbox field.

    :name field: Field should a given field.
    :type field: django.forms.boundfield.BoundField
    """
    return field.field.widget.__class__.__name__ in (
        'CheckboxInput', 'CheckboxSelectMultiple')


@register.inclusion_tag('django_mailman3/bootstrap/form.html',
                        takes_context=True)
def bootstrap_form(context, form, button=None):
    """
    Given a form, renders it using the bootstrapped template.
    """
    return dict(
        form=form,
        button=button,
        )


@register.inclusion_tag('django_mailman3/bootstrap/form-horizontal.html',
                        takes_context=True)
def bootstrap_form_horizontal(
        context, form, size_left=2, size_right=8, button=None,
        fold_class='sm'):
    """
    Given a form object, renders the form horizontally using the bootstrap
    template.
    """
    return dict(
        form=form,
        size_left=size_left,
        size_right=size_right,
        button=button,
        fold_class=fold_class,
        )
