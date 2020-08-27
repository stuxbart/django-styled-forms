from ..styles import BootstrapStyle, SemanticUIUIStyle, Style, styles
from django.forms import FileField
from django.forms.widgets import CheckboxInput, RadioSelect
from django.forms import widgets
from django.core.exceptions import ValidationError
from types import MethodType
from django.utils.html import conditional_escape, mark_safe


class StyledForm:
    """
    Base class for all styled forms. Override is_valid, _clean_fields, _html_output
    methods from django.form.Form class.
    Added the as_div method which is used as default in __str__.
    Property style holds all styling classes and display methods.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user_style = getattr(self, "Style", None)
        if user_style is not None:
            s = getattr(self.Style, "style", None)
            if s is not None:
                style = styles.get_style(s)
                if style is not None:
                    props = dict(style.__dict__)
                    for key, value in dict(user_style.__dict__).items():
                        props[key] = value
                    new_Style = type("NewStyle", (), props)
                    self.style = Style(style=new_Style)
                else:
                    raise Exception("Style '%s' not found" % s)
            else:
                self.style = Style(style=user_style)
        else:
            self.style = Style(style=user_style)

        if not hasattr(self, "input_valid_cssclass"):
            self.input_valid_cssclass = self.style.css_classes["valid_input"]

        if not hasattr(self, "input_invalid_cssclass"):
            self.input_invalid_cssclass = self.style.css_classes["invalid_input"]

        # Set css classes to the inputs
        for name, field in self.fields.items():
            if isinstance(field.widget, CheckboxInput):
                try:
                    field.widget.attrs['class'] += " %s" % self.style.css_classes["input_checkbox"]
                except KeyError:
                    field.widget.attrs['class'] = self.style.css_classes["input_checkbox"]
            elif isinstance(field.widget, widgets.FileInput) or isinstance(field.widget, widgets.ClearableFileInput):
                try:
                    field.widget.attrs['class'] += " %s" % self.style.css_classes["input_file"]
                except KeyError:
                    field.widget.attrs['class'] = self.style.css_classes["input_file"]
            else:
                try:
                    field.widget.attrs['class'] += " %s" % self.style.css_classes["input"]
                except KeyError:
                    field.widget.attrs['class'] = self.style.css_classes["input"]

        # Override methods
        self._clean_fields = MethodType(StyledForm._clean_fields, self)
        self.is_valid = MethodType(StyledForm.is_valid, self)
        self._html_output = MethodType(StyledForm._html_output, self)

    def __str__(self):
        return self.as_div()

    def is_valid(self):
        """
        Return True if the form has no errors, or False otherwise.
        Sets additional form validation style classes.
        """
        self.style.css_classes['form'] += " " + self.style.css_classes['validated_form']
        valid = self.is_bound and not self.errors
        if valid:
            self.style.css_classes['form'] += " " + self.style.css_classes['valid_form']
        else:
            self.style.css_classes['form'] += " " + self.style.css_classes['invalid_form']
        return valid

    def _clean_fields(self):
        """
        The only difference from django.form.Form._clean_fields is adding css classes to the fields.
        """
        for name, field in self.fields.items():
            if field.disabled:
                value = self.get_initial_for_field(field, name)
            else:
                value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))
            try:
                if isinstance(field, FileField):
                    initial = self.get_initial_for_field(field, name)
                    value = field.clean(value, initial)
                else:
                    value = field.clean(value)
                self.cleaned_data[name] = value
                if hasattr(self, 'clean_%s' % name):
                    value = getattr(self, 'clean_%s' % name)()
                    self.cleaned_data[name] = value
                field.widget.attrs['class'] += " %s" % self.input_valid_cssclass
            except ValidationError as e:
                self.add_error(name, e)
                field.widget.attrs['class'] += " %s" % self.input_invalid_cssclass

    def _html_output(self, normal_row, special_rows, error_row, row_ender, help_text_html, errors_on_separate_row):
        """Output HTML. Used by as_table(), as_ul(), as_p(), as_div()."""
        top_errors = self.non_field_errors().copy()
        output = self.style.grid
        hidden_fields = []

        for name, field in self.fields.items():
            html_class_attr = ''
            bf = self[name]
            bf_errors = self.error_class(bf.errors).as_text()
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend(
                        ['(Hidden field %(name)s) %(error)s' % {'name': name, 'error': str(e)}
                         for e in bf_errors.splitlines(keepends=False)])
                hidden_fields.append(str(bf))
            else:
                # Create a 'class="..."' attribute if the row should have any
                # CSS classes applied.
                css_classes = bf.css_classes()
                if css_classes:
                    html_class_attr = ' class="%s"' % css_classes

                if errors_on_separate_row and bf_errors:
                    output.set_error(name, error_row % str(bf_errors))

                if bf_errors:
                    error_class = self.style.css_classes['invalid_input']
                else:
                    error_class = ""
                if bf.label:
                    label = conditional_escape(bf.label)

                    # change label attrs base on input type
                    if isinstance(field.widget, CheckboxInput):
                        attrs = {"class": self.style.css_classes['label_checkbox']}
                        label_suffix = ""
                    else:
                        attrs = {"class": self.style.css_classes['label']}
                        label_suffix = ":"
                    label = bf.label_tag(label, attrs=attrs, label_suffix=label_suffix) or ''

                else:
                    label = ''

                if field.help_text:
                    help_text = help_text_html % field.help_text
                else:
                    help_text = ''

                # Different row format for different inputs
                if isinstance(field.widget, CheckboxInput) or isinstance(field.widget, RadioSelect):
                    row = special_rows["checkbox"]
                elif isinstance(field.widget, widgets.FileInput):
                    row = special_rows["file"]
                else:
                    row = normal_row
                output[name] = (row % {
                    'errors': bf_errors,
                    'error_class': error_class,
                    'label': label,
                    'field': bf,
                    'help_text': help_text,
                    'html_class_attr': html_class_attr,
                    'css_classes': css_classes,
                    'field_name': bf.html_name,
                })

        if top_errors:
            output['top_errors'] = error_row % top_errors

        if hidden_fields:  # Insert any hidden fields in the last row.
            str_hidden = ''.join(hidden_fields)

            output.rendered_hidden_fields = str_hidden
        return mark_safe(output.get_html())

    def as_div(self):
        return self._html_output(
            normal_row=self.style.get_normal_row(),
            special_rows={
                "checkbox": self.style.get_checkbox_row(),
                "file": self.style.get_file_row()
            },
            error_row=self.style.get_error_row(),
            row_ender='</div>',
            help_text_html=' <small class="form-text text-muted">%s</small>',
            errors_on_separate_row=self.style.errors_on_separate_row,
        )


class BootstrapForm(StyledForm):
    """StyledForm with Bootstrap classes"""
    def __init__(self, *args, **kwargs):
        if hasattr(self, "Style"):
            setattr(self.Style, "style", "bootstrap")
        else:
            class NewStyle:
                style = "bootstrap"
            setattr(self, "Style", NewStyle)
        super().__init__(*args, **kwargs)


class SemanticUIForm(StyledForm):
    """StyledForm with Semantic UI classes"""
    def __init__(self, *args, **kwargs):
        if hasattr(self, "Style"):
            setattr(self.Style, "style", "semanticui")
        else:
            class NewStyle:
                style = "semanticui"
            setattr(self, "Style", NewStyle)
        super().__init__(*args, **kwargs)
