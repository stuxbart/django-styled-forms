============
Styled Forms
============

Styled Forms is Django app which provide easy way to add styling to forms.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "styled_forms" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'styled_forms',
    ]

2. Import and use decorators::

    from django import forms
    from styled_forms.decorators import bootstrap_style_form

    @bootstrap_style_form
    class TestForm(forms.Form):
        ...


Or import form style class::

    from django import forms
    from styled_forms.forms import BootstrapForm

    class TestForm(BootstrapForm, forms.Form):
        ...

You can add Style class with custom properties to the form::

    class TestForm(SemanticUIForm, forms.Form):
        name = forms.CharField()
        password = forms.CharField(widget=forms.PasswordInput())

    class Style:
        grid = [
            [("name", 8), ("password", 8)] # 16 per row for Semantic UI, 12 for Bootstrap
        ]
        css_classes = {
            "form": "ui form custom",
        }

Styled forms have additional as_div method which is default render class.
In template you can simply write::

    <form action="" class="{{ form.get_form_class }}">
        {{ form }}
        <button type="submit" class="ui button">Submit</button>
    </form>

