from django import forms
from .forms import (
    StyledForm,
    BootstrapForm,
    SemanticUIForm
)
from ..decorators import (
    styled_form,
    bootstrap_style_form,
    semanticui_style_form,
)
from django.core.exceptions import ValidationError
from django.forms import widgets


@bootstrap_style_form
class TestForm(forms.Form):
    name = forms.CharField(required=True)
    body = forms.CharField(widget=forms.Textarea())
    xe = forms.CharField(widget=forms.HiddenInput())
    check = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].help_text = 'Hold down "Control" to select more.'

    class Style:
        # style = "semanticui"
        grid = [
            [('name', 6), ('check', 6)],
            [('body', 12)]
        ]


@styled_form
class TestForm1(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Email"}),
        label="Email"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
        label="Password"
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "1234 Main St"}),
        label="Address"
    )
    address2 = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Apartment, studio, or floor"}),
        label="Address 2"
    )
    city = forms.CharField(
        label="City"
    )
    state = forms.ChoiceField(
        choices=(('xd', 'Choose...'),),
        label="State"
    )
    zip = forms.CharField(
        label="Zip"
    )
    check = forms.BooleanField(
        label="Check me out"
    )

    def clean_password(self):
        raise ValidationError("xD")

    class Style:
        style = "bootstrap"
        grid = [
            [('email', 6), ('password', 6)],
            [('address', 12)],
            [('address2', 12)],
            [('city', 6), ('state', 4), ('zip', 2)],
            [('check', 8)]
        ]
        errors_on_separate_row = False


# @bootstrap_form
class TestForm2(SemanticUIForm, forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "First Name"}),
        label="First Name",
        required=False
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Last name"}),
        label="Last Name",
        required=False
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Username"}),
        label="Username",
        required=False
    )
    city = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "City"}),
        label="City",
        required=False
    )
    state = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "State"}),
        label="State",
        required=False
    )
    zip = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Zip"}),
        label="Zip",
        required=False
    )
    check = forms.BooleanField(
        label="Agree to terms and conditions",
        required=False
    )

    def clean_username(self):
        raise ValidationError("Please choose a username.")

    def clean_city(self):
        raise ValidationError("Please provide a valid city.")

    def clean_state(self):
        raise ValidationError("Please provide a valid state.")

    def clean_zip(self):
        raise ValidationError("Please provide a valid zip.")

    def clean_check(self):
        raise ValidationError("You must agree before submitting.")

    class Style:
        # style = "bootstrap"
        grid = [
            [('first_name', 4), ('last_name', 4), ('username', 4)],
            [('city', 6), ('state', 4), ('zip', 2)],
            [('check', 10)]
        ]
        errors_on_separate_row = False

@styled_form
class TestForm3(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "mx-sm-3"}),
        label="Password",
        help_text="Must be 8-20 characters long."
    )

    class Style:
        # style = "semanticui"
        css_classes = {
            "form": "ui form inline"
        }


@styled_form
class TestForm4(forms.Form):
    name = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "mb-2 mr-sm-2"}),
    )
    username = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "mb-2 mr-sm-2"}),
    )
    check = forms.BooleanField(
        label="Remember me",
    )
    date = forms.DateTimeField(widget=widgets.SplitDateTimeWidget())

    class Style:
        style = "semanticui"

        grid = [
            [('name', 6), ('username', 5), ("check", 5)],
            [('date', 6)]
        ]
        use_form_group_div = False
