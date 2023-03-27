from dataclasses import field
from django import forms
from .models import News, Comments, TAGS

# class NewsForm(forms.Form):
#     article = forms.CharField()
#     body = forms.CharField(widget=forms.Textarea)

class NewsModelForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['article',
                  'body',
                  'image',
                  'tag',
                ]
        widgets = {
            'tag':forms.Select()
        }
    
    def clean_article(self):
        data = self.cleaned_data.get('article')
        if len(data) < 5:
            raise forms.ValidationError('article is not long enough')
        return data

class CommentaryModelForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = [
            'text'
        ]

class SearchForm(forms.Form):
    searchtag = forms.MultipleChoiceField(choices=TAGS, widget=forms.CheckboxSelectMultiple, label="Фильтры")

        

