from django.core.exceptions import ValidationError
from .forms.forms import StyledForm


def bootstrap_validation(function):
    """
    Add "is-valid" or "is-invalid" css class to the field.
    """

    def _validation(*args, **kwargs):
        field_name = function.__name__.split("_")[1]
        form = args[0]
        try:
            result = function(*args, **kwargs)
            try:
                form.fields[field_name].widget.attrs['class'] += " is-valid"
            except KeyError:
                form.fields[field_name].widget.attrs['class'] = "is-invalid"
            return result

        except ValidationError as e:
            try:
                form.fields[field_name].widget.attrs['class'] += " is-invalid"
            except KeyError:
                form.fields[field_name].widget.attrs['class'] = "is-invalid"
            raise ValidationError(e)

    return _validation


def styled_form(Cls):
    """
    Class decorator.
    Change Cls form class to StyledForm.
    """
    NewCls = type("NewCls", (StyledForm, Cls), {})
    return NewCls


def bootstrap_style_form(Cls):
    """
    Class decorator.
    Change Cls form class to StyledForm with Bootstrap classes.
    """
    if hasattr(Cls, "Style"):
        props = dict(Cls.Style.__dict__)
        props['style'] = "bootstrap"
        NewStyle = type("NewStyle", (), props)

    else:
        class NewStyle:
            style = "bootstrap"
    NewCls = type("NewCls", (StyledForm, Cls), {"Style": NewStyle})
    return NewCls


def semanticui_style_form(Cls):
    """
    Class decorator.
    Change Cls form class to StyledForm with Semantic UI classes.
    """
    if hasattr(Cls, "Style"):
        props = dict(Cls.Style.__dict__)
        props['style'] = "semanticui"
        NewStyle = type("NewStyle", (), props)

    else:
        class NewStyle:
            style = "semanticui"
    NewCls = type("NewCls", (StyledForm, Cls), {"Style": NewStyle})
    return NewCls

