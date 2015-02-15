__author__ = 'BCCUB002'
from django import forms
from django.contrib.auth.models import User
from Users.models import Page, Category, UserProfile
from Packages.models import Service

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        exclude = ('category',)
        #or specify the fields to include (i.e. not include the category field)
        #fields = ('title', 'url', 'views')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    fname = forms.CharField(max_length=20, help_text="Please enter first name", label="First Name")
    lname = forms.CharField(max_length=20, help_text="Please enter last name", label="Last Name")
    #meta describes additional properties about the particular modelForm class it belongs to
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'fname', 'lname')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')

class ServiceForm(forms.ModelForm):
    service = forms.ChoiceField(widget=forms.RadioSelect)
    class Meta:
        model = Service
        fields = ('name', 'description', 'price', 'term_fee')

class DisplayForm(forms.ModelForm):
    services = forms.CharField(max_length=120, label="Current Services")
    class Meta:
        model = Service
        fields = ('name', 'description', 'price', 'term_fee')

class DeleteServiceForm(forms.ModelForm):
    services = forms.CharField(max_length=120, label="Current Services")
    class Meta:
        model = Service
        fields = ('name', 'description', 'price', 'term_fee')