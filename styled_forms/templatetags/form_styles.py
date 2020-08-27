from django.template.defaulttags import register
from ..forms import StyledForm
from ..styles import styles


@register.filter
def custom_style(form, style):
    """
    Template filter
    Add form styling to the form instance.
    :param form: form instance
    :param style: registered style name
    :return: new form
    """
    if not hasattr(form, "style"):

        Style = styles.get_style(style)
        if hasattr(form, "Style"):

            if Style is not None:
                props = dict(Style.__dict__)
                for key, value in dict(form.Style.__dict__).items():
                    props[key] = value
            else:
                props = dict(form.Style.__dict__)
            NewStyle = type("NewStyle", (), props)

        else:

            if Style is not None:
                NewStyle = Style
            else:
                return form

        form_data = dict(form.__dict__)
        form_data["Style"] = NewStyle

        new_form = type("NewCls", (StyledForm, form.__class__), form_data)
        obj = new_form()

        for key, value in form_data.items():
            setattr(obj, key, value)

        return obj

    return form
