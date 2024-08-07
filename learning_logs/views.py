from django.shortcuts import render, redirect, get_object_or_404
from .models import Topic, Entry, Comment
from .forms import TopicForm, EntryForm, CommentForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Q


#проверка, что пользователь связан с темой
def check_topic_owner(topic, request):
    if topic.public == False:
        if topic.owner != request.user:
            raise Http404
    

# Create your views here.

def index(request):
    #домашняя страница приложения Learning Log
    return render(request, 'learning_logs/index.html')
    

def topics(request):
    #выводит список тем (проверка на авторизованность)
    if request.user.is_authenticated:
        topics = Topic.objects.filter(Q(owner=request.user) | Q(public = True)).order_by('date_added')
    else:
        topics = Topic.objects.filter(public = True).order_by('date_added')
    context = {'topics':topics}
    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    #Выводит одну тему и все ее записи
    topic = get_object_or_404(Topic, id=topic_id)
    #проверка того, что тема принадлежит текущему пользователю
    check_topic_owner(topic, request)
    
    entries = topic.entry_set.order_by('-date_added')
    #знак - это сортировка в обратном порядке по времени
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


def new_topic(request):
    #определяет новую тему
    if request.method != 'POST':
        #данные не отправлялись, создается пустая строка
        form = TopicForm()
    else:
        #данные отправлены POST, обработать данные
        form = TopicForm(data=request.POST)
        if form.is_valid(): #если всё правильно заполнено
            new_topic = form.save(commit=False)
            if request.user.is_authenticated:
                new_topic.owner = request.user
            else:
                new_topic.owner = User.objects.get(username = 'anonymous')
                new_topic.public = True
            new_topic.save() #сохраняем в базу данных
            return redirect('learning_logs:topics')
            
    context = {'form':form} #создаем форму
    return render(request, 'learning_logs/new_topic.html', context)


def new_entry(request, topic_id):
    #определяет новую запись по конкретной теме
    topic = get_object_or_404(Topic, id=topic_id)
    check_topic_owner(topic, request)
    if request.method != 'POST':
        #данные не отправлялись, создается пустая строка
        form = EntryForm()
    else:
        #данные отправлены POST, обработать данные
        form = EntryForm(data=request.POST)
        if form.is_valid(): #если всё правильно заполнено
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            #проверка на зарегистрированного пользователя
            if request.user.is_authenticated:
                new_entry.owner = request.user
            else:
                new_entry.owner = User.objects.get(username = 'anonymous')
            
            new_entry.save() #сохраняем в базу данных
            return redirect('learning_logs:topic', topic_id=topic_id)
            
    context = {'topic': topic, 'form':form} #создаем форму
    return render(request, 'learning_logs/new_entry.html', context)


def edit_entry(request, entry_id):
    #редактируем определённую запись
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    #Проверка на текущего пользователя
    check_topic_owner(topic, request)
    if request.method != 'POST':
        #исходный запрос, форма заполняется данными текущей записи
        form = EntryForm(instance=entry) #создаёт форму с заполненной информацией
    else:
        #данные отправлены POST, обработать данные
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid(): #если всё правильно заполнено
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
            
    context = {'entry': entry, 'topic': topic, 'form':form} #создаем форму
    return render(request, 'learning_logs/edit_entry.html', context)


def open_entry(request, entry_id):
    #Выводит одну запись и ее комментарии
    entry = get_object_or_404(Entry, id=entry_id)
    #выводит все комментарии к записи (знак - это сортировка в обратном порядке по времени)
    comments = entry.comment_set.order_by('-date_added')
    
    if request.method != 'POST':
        #данные не отправлялись, создается пустая строка
        form = CommentForm()
    else:
        #данные отправлены POST, обработать данные
        form = CommentForm(data=request.POST)
        if form.is_valid(): #если всё правильно заполнено
            new_comment = form.save(commit=False)
            new_comment.entry = entry
            #проверка на зарегистрированного пользователя
            if request.user.is_authenticated:
                new_comment.owner = request.user
            else:
                new_comment.owner = User.objects.get(username = 'anonymous')
            
            new_comment.save() #сохраняем в базу данных
            return redirect(request.path) #обновляем страницу, чтобы форма очистилась
            
    context = {'entry': entry, 'comments': comments, 'form': form}
    return render(request, 'learning_logs/open_entry.html', context)
           
           
    

    
