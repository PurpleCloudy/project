from dataclasses import field
from django import forms
from .models import News, Comments, TAGS

FIELDS_SEARCH = [
    ('ART','article'),
    ('AUB','author_book'),
    ('AUT', 'author'),
]

class NewsModelForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['article',
                  'author_book',
                  'body',
                  'image',
                  'tag',
                  'quality',
                  'is_in'
                ]
        widgets = {
            'tag':forms.Select(),
            'quality':forms.Select()
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

class FilterForm(forms.Form):
    searchtag = forms.MultipleChoiceField(choices=TAGS, widget=forms.CheckboxSelectMultiple, label="Фильтры")

class SearchForm(forms.Form):
    searchinput = forms.CharField(max_length=100, label='Введите название')
