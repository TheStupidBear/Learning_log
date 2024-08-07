from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
    # Тема, которую изучает пользователь
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True) #устанавливает текущее время
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=True)

    def __str__(self):
        #возвращает строковое представление модели
        return self.text
        



class Entry(models.Model):
    #информация, изученная пользователем по теме
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = 'entries'
    
    def __str__(self):
        return self.name
        
        
class Comment(models.Model):
    #комментарии к записям
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        if len(self.text) > 50:
            return f"{self.text[:50]}..."
        else:
            return f"{self.text[:50]}"