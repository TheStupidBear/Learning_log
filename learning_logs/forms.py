
from django import forms
from .models import Topic, Entry, Comment

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text', 'public']
        labels = {'text':''}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['name','text']
        labels = {'text':'', 'name':'Имя записи:'}
        widgets = {'text':forms.Textarea(attrs={'cols':80})}
        #указывает, чтобы было 80 столбцов в форме

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text':''}
        widgets = {'text':forms.Textarea(attrs={'cols':80})}
        #указывает, чтобы было 80 столбцов в форме

