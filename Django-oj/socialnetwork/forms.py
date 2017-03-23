from django import forms
from django.contrib.auth.models import User
from socialnetwork.models import Entry, Posts, Comments
# forms.py
from django.forms.widgets import FileInput
from django.forms import ModelForm, FileInput
from PIL import Image
MAX_UPLOAD_SIZE = 2500000

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name  = forms.CharField(max_length=20)
    username   = forms.CharField(max_length = 20)
    email      = forms.CharField(max_length=50,
                                 widget = forms.EmailInput())
    password1  = forms.CharField(max_length = 200, 
                                 label='Password', 
                                 widget = forms.PasswordInput())
    password2  = forms.CharField(max_length = 200, 
                                 label='Confirm password',  
                                 widget = forms.PasswordInput())


    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data


    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username

class AddForm(forms.Form):
    post = forms.CharField(max_length = 160)

    def clean(self):
        cleaned_data = super(AddForm,self).clean()

        return cleaned_data

    def clean_post(self):
        cleaned_data = self.cleaned_data.get('post')
        
        if not cleaned_data:
            raise forms.ValidationError("need to use post method")
        if len(cleaned_data) == 0:
            raise forms.ValidationError("You must write a post first")
        if len(cleaned_data) >160:
            raise forms.ValidationError("Your post should be within 160 characters")
        return cleaned_data    

class CommentForm(forms.Form):
    item = forms.CharField(max_length = 160)

    def clean(self):
        cleaned_data = super(CommentForm,self).clean()

        return cleaned_data

    def clean_item(self):
        cleaned_data = self.cleaned_data.get('item')
        
        if not cleaned_data:
            raise forms.ValidationError("need to use post method")
        if len(cleaned_data) == 0:
            raise forms.ValidationError("You must write a comment first")
        if len(cleaned_data) >160:
            raise forms.ValidationError("Your comment should be within 160 characters")
        return cleaned_data 

class EditForm(forms.ModelForm):
    picture = forms.FileField(widget=forms.FileInput)
    class Meta:
        model = Entry
        fields = ['picture','first_name','last_name','age','bio']
        # fields = ['picture','age','bio']

    def clean(self):

        cleaned_data = super(EditForm,self).clean()
        return cleaned_data

    def clean_age(self):
        age = self.cleaned_data.get('age')

        if not age:
            raise forms.ValidationError("prodive your age")
        if not age.isdigit():
            raise forms.ValidationError("age must be an integer")
        return age

    def clean_picture(self):
        picture = self.cleaned_data['picture']

        if not picture:
            raise forms.ValidationError('invalid image type')   
        try:
            img = Image.open(picture)
        except:
            raise forms.ValidationError('invalid image type')
        if picture.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return picture




# from django import forms
# from django.contrib.auth.models import User
# from socialnetwork.models import Entry, Posts

# MAX_UPLOAD_SIZE = 2500000
# class RegistrationForm(forms.Form):
#     first_name = forms.CharField(max_length=20)
#     last_name  = forms.CharField(max_length=20)
#     username   = forms.CharField(max_length = 20)
#     password1  = forms.CharField(max_length = 200, 
#                                  label='Password', 
#                                  widget = forms.PasswordInput())
#     password2  = forms.CharField(max_length = 200, 
#                                  label='Confirm password',  
#                                  widget = forms.PasswordInput())


#     # Customizes form validation for properties that apply to more
#     # than one field.  Overrides the forms.Form.clean function.
#     def clean(self):
#         # Calls our parent (forms.Form) .clean function, gets a dictionary
#         # of cleaned data as a result
#         cleaned_data = super(RegistrationForm, self).clean()

#         # Confirms that the two password fields match
#         password1 = cleaned_data.get('password1')
#         password2 = cleaned_data.get('password2')
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords did not match.")

#         # We must return the cleaned data we got from our parent.
#         return cleaned_data


#     # Customizes form validation for the username field.
#     def clean_username(self):
#         # Confirms that the username is not already present in the
#         # User model database.
#         username = self.cleaned_data.get('username')
#         if User.objects.filter(username__exact=username):
#             raise forms.ValidationError("Username is already taken.")

#         # We must return the cleaned data we got from the cleaned_data
#         # dictionary
#         return username

# class AddForm(forms.Form):
#     post = forms.CharField(max_length = 60)

#     def clean(self):
#         cleaned_data = super(AddForm,self).clean()

#         if len(cleaned_data) == 0:
#             raise forms.ValidationError("You must write a post first")
#         return cleaned_data

# class EditForm(forms.ModelForm):

#     class Meta:
#         model = Entry
#         fields = ['picture','first_name','last_name','age','bio']

#     def clean(self):

#         cleaned_data = super(EditForm , self).clean()
#         return cleaned_data

#     def clean_age(self):

#         age = self.cleaned_data['age']

#         if not age.isdigit():
#             raise forms.ValidationError("age must be an integer")
#         return age

#     def clean_picture(self):

#         picture = self.cleaned_data['picture']
#         if not picture:
#             raise forms.ValidationError('You must upload a picture')
#         if not picture.content_type or not picture.content_type.startswith('image'):
#             raise forms.ValidationError('File type is not image')
#         if picture.size > MAX_UPLOAD_SIZE:
#             raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
#         return picture


