from .forms.forms import StyledForm


def create_style(Style):
    """Create form decorator with custom styling"""
    def _custom_style_form(Cls):
        if hasattr(Cls, "Style"):
            props = dict(Style.__dict__)
            for key, value in dict(Cls.Style.__dict__).items():
                props[key] = value
            NewStyle = type("NewStyle", (), props)

        else:
            NewStyle = Style
        NewCls = type("NewCls", (StyledForm, Cls), {"Style": NewStyle})
        return NewCls
    return _custom_style_form
