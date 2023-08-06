# -*- coding: utf-8 -*-
# Copyright (C) 2017-2018 by the Free Software Foundation, Inc.
#
# This file is part of Django-Mailman.
#
# HyperKitty is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# HyperKitty is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# Django-Mailman.  If not, see <http://www.gnu.org/licenses/>.
#

from django.test import SimpleTestCase
from django.template import Context, Template
from django.forms import Form, EmailField, DateField, ChoiceField
from django.forms.widgets import CheckboxInput

from django_mailman3.templatetags.bootstrap_tags import (
    fieldtype, fieldtype_is, is_checkbox)


class TestForm(Form):
    datetime = DateField()
    email = EmailField()
    choices = ChoiceField(choices=('yes', 'no'), widget=CheckboxInput)


class TestBootstrapTags(SimpleTestCase):

    def setUp(self):
        self.form = TestForm()

    def test_add_form_control(self):
        # Given a field the field class has 'form-control' in it.
        context = Context({'form': self.form})
        template = Template(
            '{% load bootstrap_tags %}'
            '{% for field in form.visible_fields %}'
            '{{ field | add_form_control }} <br />'
            '{% endfor %}')
        rendered_template = template.render(context=context)
        datetime_field = 'class="form-control"'
        self.assertTrue(datetime_field in rendered_template)

    def test_fieldtype(self):
        # Fieldtype takes a bounded formfield and returns it's type.
        fields = [fieldtype(field) for field in self.form.visible_fields()]
        self.assertEqual(sorted(fields),
                         ['CheckboxInput', 'DateInput', 'EmailInput'])
        # If the wrong instance of the field is passed.
        with self.assertRaises(AssertionError):
            fieldtype(self.form.fields['email'])

    def test_fieldtype_is(self):
        # Fields should return true for all of it's parent classes in
        # the hierarchy.
        for field in self.form.visible_fields():
            if field.name == 'datetime':
                self.assertTrue(fieldtype_is(field, 'DateInput'))
                self.assertTrue(fieldtype_is(field, 'DateTimeBaseInput'))
                self.assertTrue(fieldtype_is(field, 'TextInput'))
                self.assertFalse(fieldtype_is(field, 'RadioSelect'))
            if field.name == 'email':
                self.assertTrue(fieldtype_is(field, 'EmailInput'))
                self.assertTrue(fieldtype_is(field, 'Input'))
            if field.name == 'choices':
                self.assertTrue(fieldtype_is(field, 'CheckboxInput'))

    def test_is_checkbox(self):
        # There should a checkbox in our current field.
        fields = list(self.form.visible_fields())
        self.assertEqual(sorted(map(is_checkbox, fields)),
                         [False, False, True])
        for field in self.form.visible_fields():
            if field.name == 'choices':
                self.assertTrue(is_checkbox(field))

    def test_boostrap_form(self):
        # Test that bootstrap_form renders the form without errors.
        context = Context({'title': 'My Title',
                           'form': self.form,
                           'button': "Yes"})
        # Test the template is rendered.
        template = Template(
            '{% load bootstrap_tags %}'
            '<form> {% bootstrap_form form %}')
        rendered_template = template.render(context=context)
        label_field = '''
<label class="control-label" for="id_datetime">
    Datetime
</label>'''
        self.assertInHTML(label_field, rendered_template)
        # Now render the form with a submit buttom
        template = Template(
            '{% load bootstrap_tags %}'
            '<form> {% bootstrap_form form=form button=button %}')
        rendered_template = template.render(context=context)
        button_html = '''
<div class="form-group">
    <button class="btn btn-primary" type="submit">Yes</button>
</div>
'''
        self.assertInHTML(button_html, rendered_template)

    def test_boostrap_form_horizontal(self):
        # Test that bootstrap_form_horizontal renders the form and includes the
        # submit button.
        context = Context({'title': 'My Title',
                           'form': self.form,
                           'button': "Yes"})
        template = Template(
            '{% load bootstrap_tags %}'
            '<form> {% bootstrap_form_horizontal form=form button=button%}')
        rendered_template = template.render(context=context)
        self.assertInHTML(
            '<button class="btn btn-primary" type="submit">Yes</button>',
            rendered_template)
