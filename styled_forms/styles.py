from types import MethodType

num_to_words = {
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
    11: "eleven",
    12: "twelve",
    13: "thirteen",
    14: "fourteen",
    15: "fifteen",
    16: "sixteen"
}


class Grid:
    """
    Base Grid class used for rendering fields in appropriate position.
    """
    def __init__(self, grid=None, errors_on_separate_row=False):
        self.grid = grid
        self.rendered_fields = {}
        self.rendered_hidden_fields = ""
        self.rendered_errors = {}
        self.errors_on_separate_row = errors_on_separate_row

    def __setitem__(self, key, value):
        self.rendered_fields[key] = value

    def items(self):
        return self.rendered_fields.items()

    def get_html(self):
        """Return form html"""
        return '\n'.join(self.rendered_fields.values())

    def set_error(self, name, value):
        self.rendered_errors[name] = value


class BootstrapGrid(Grid):
    """Override get_html method to use Bootstrap grid"""
    def get_html(self):
        if self.grid:
            output = []
            a = output.append
            for row in self.grid:
                a("<div class='form-row'>\n")
                for field in row:
                    if isinstance(field, tuple) or isinstance(field, list):
                        f = field[0]
                        width = field[1]
                        if isinstance(width, int):
                            if not 1 <= width <= 12:
                                raise ValueError("Bootstrap field width must be between 1 and 12")
                            width_class = f"col-{width}"
                        elif isinstance(width, str):
                            width_class = width
                        else:
                            raise TypeError("Wrong width type")
                    else:
                        f = field
                        width_class = "col"
                    a(f"<div class='{width_class}'>\n")
                    a(self.rendered_fields[f])
                    a("</div>\n")
                a("</div>\n")
            a("<div class='form-row'>\n")
            a(self.rendered_hidden_fields)
            a("</div>\n")
            return ''.join(output)
        else:
            return '\n'.join(self.rendered_fields.values())


class SemanticUIGrid(Grid):
    """
    Override get_html method to use Semantic UI grid.
    """
    def get_html(self):
        if self.grid:
            output = []
            a = output.append
            for row in self.grid:
                a("<div class='field'>\n")
                a("<div class='fields'>\n")
                for field in row:
                    if isinstance(field, tuple) or isinstance(field, list):
                        f = field[0]
                        width = field[1]
                        if isinstance(width, int):
                            if not 1 <= width <= 16:
                                raise ValueError("Semantic-UI field width must be between 1 and 16")
                            width_class = f"{num_to_words[width]} wide field"
                        elif isinstance(width, str):
                            width_class = f"{width} wide field"
                        else:
                            raise TypeError("Wrong width type")
                    else:
                        f = field
                        width_class = "field"
                    a(f"<div class='{width_class}'>\n")
                    a(self.rendered_fields[f])
                    if self.errors_on_separate_row:
                        if f in self.rendered_errors:
                            a(self.rendered_errors[f])
                    a("</div>\n")

                a("</div>\n")
                a("</div>\n")
            a("<div class='form-row'>\n")
            a(self.rendered_hidden_fields)
            a("</div>\n")
            return ''.join(output)
        else:
            output = []
            a = output.append
            for name, value in self.rendered_fields.items():
                a(value)
                if name in self.rendered_errors:
                    a(self.rendered_errors[name])
            return '\n'.join(output)


class Style:
    """
    Style class which has all form styling classes and render methods.
    """
    css_classes = {
        "form": "form",
        "validated_form": "validated-form",
        "valid_form": "",
        "invalid_form": "",

        "input": "input",
        "input_checkbox": "input-checkbox",
        "input_file": "input-file",

        "label": "label",
        "label_checkbox": "label-checkbox",

        "input_group": "input-group",
        "input_group_checkbox": "input-group-checkbox",

        "valid_input": "valid-input",
        "invalid_input": "invalid-input",

    }
    use_form_group_div = True
    fields_per_row = 1
    grid_class = Grid
    errors_on_separate_row = False

    def __init__(self, style=None, css_classes=None):

        if hasattr(style, "css_classes"):
            css_classes = style.css_classes

        if css_classes is not None:
            for key, value in self.css_classes.items():
                v = css_classes.get(key, None)
                if v is not None:
                    self.css_classes[key] = v

        if style is not None:
            for prop, value in style.__dict__.items():
                if not prop.startswith("__"):
                    if prop not in ['grid', 'css_classes']:
                        if callable(value):
                            setattr(self, prop, MethodType(value, self))
                        else:
                            if hasattr(self, prop):
                                setattr(self, prop, value)

        if style:
            if hasattr(style, 'grid'):
                if hasattr(style, "grid_class"):
                    self.grid = style.grid_class(style.grid, self.errors_on_separate_row)
                else:
                    self.grid = self.grid_class(style.grid, self.errors_on_separate_row)
            else:
                if hasattr(style, "grid_class"):
                    self.grid = style.grid_class(None, self.errors_on_separate_row)
                else:
                    self.grid = self.grid_class(None, self.errors_on_separate_row)
        else:
            self.grid = self.grid_class(None, self.errors_on_separate_row)

    def render(self):
        self.grid.get_html()

    def get_default_row(self):
        return f"""
        <div class="{self.css_classes['input_group']}">
            %(label)s
            %(field)s
            %(errors)s
            %(help_text)s
        </div>
        """

    def get_normal_row(self):
        """Return html for normal input"""
        return self.get_default_row()

    def get_checkbox_row(self):
        """Return html for checkbox input"""
        return self.get_default_row()

    def get_error_row(self):
        """Return html for error display"""
        return "%s"

    def get_file_row(self):
        """Return html for file input"""
        return self.get_default_row()

    def get_form_cssclass(self):
        """Return form css classes"""
        return self.css_classes['form']


class Bootstrap:
    css_classes = {
        "form": "",
        "validated_form": "",
        "valid_form": "",
        "invalid_form": "",

        "input": "form-control",
        "input_checkbox": "form-check-input",
        "input_file": "form-control-file",

        "label": "",
        "label_checkbox": "form-check-label",
        "label_file": "custom-file-label",

        "input_group": "form-group",
        "input_group_checkbox": "form-check",

        "valid_input": "is-valid",
        "invalid_input": "is-invalid",

    }
    grid_class = BootstrapGrid
    errors_on_separate_row = False

    def get_normal_row(self):
        return f"""
        {f'<div class="{self.css_classes["input_group"]}">' if self.use_form_group_div else ''}
            %(label)s
            %(field)s
            <div class="invalid-feedback">
                %(errors)s
            </div>
            %(help_text)s
        {'</div>' if self.use_form_group_div else ''}
        """

    def get_checkbox_row(self):
        return f"""
        <div class="{self.css_classes["input_group"]}">
            <div class="{self.css_classes["input_group_checkbox"]}">
                %(field)s
                %(label)s
                <div class="invalid-feedback">
                    %(errors)s
                </div>
            </div>
            %(help_text)s
        </div>
        """


class BootstrapStyle(Bootstrap, Style):
    pass


class SemanticUI:
    css_classes = {
        "form": "ui form",
        "validated_form": "",
        "valid_form": "",
        "invalid_form": "error",

        "input": "",
        "input_checkbox": "",
        "input_file": "",

        "label": "",
        "label_checkbox": "",

        "input_group": "field",
        "input_group_checkbox": "ui checkbox field",

        "valid_input": "",
        "invalid_input": "error",
    }

    grid_class = SemanticUIGrid
    use_form_group_div = False
    errors_on_separate_row = True

    def get_normal_row(self):
        return f"""
        <div class="field %(error_class)s">
        %(label)s
        %(field)s
        %(help_text)s
        </div>
        """

    def get_checkbox_row(self):
        return f"""
        <div class="{self.css_classes["input_group"]}">
            <div class="{self.css_classes["input_group_checkbox"]}">
                %(field)s
                %(label)s
            </div>
            %(help_text)s
        </div>
        """

    def get_error_row(self):
        return """
        <div class="ui error message">
            <p>%s</p>
        </div>
        """


class SemanticUIUIStyle(SemanticUI, Style):
    pass


class StylesData:
    """Holds registered styles"""
    def __init__(self):
        self._styles = {}

    def get_style(self, name):
        try:
            return self._styles[name]
        except KeyError:
            return None

    def register(self, name, style):
        self._styles[name] = style


styles = StylesData()
styles.register("semanticui", SemanticUI)
styles.register("bootstrap", Bootstrap)
