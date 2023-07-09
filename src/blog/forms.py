from django import forms
from froala_editor.widgets import FroalaEditor
from .models import Article


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = "__all__"
        exclude = ['author', 'slug']
        # widgets = {
        #     "contents": FroalaEditor(),
        # }
        

