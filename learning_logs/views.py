from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

#проверка, что пользователь связан с темой
def check_topic_owner(topic, request):
    if topic.owner != request.user:
        raise Http404

# Create your views here.

def index(request):
    #домашняя страница приложения Learning Log
    return render(request, 'learning_logs/index.html')
    
@login_required
def topics(request):
    #выводит список тем
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    #запрос к базе данных на получение по времени
    context = {'topics':topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    #Выводит одну тему и все ее записи
    topic = Topic.objects.get(id=topic_id)
    #проверка того, что тема принадлежит текущему пользователю
    check_topic_owner(topic, request)

    entries = topic.entry_set.order_by('-date_added')
    #знак - это сортировка в обратном порядке по времени
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
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
            new_topic.owner = request.user
            new_topic.save() #сохраняем в базу данных
            return redirect('learning_logs:topics')
            
    context = {'form':form} #создаем форму
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    #определяет новую запись по конкретной теме
    topic = Topic.objects.get(id=topic_id)
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
            new_entry.save() #сохраняем в базу данных
            return redirect('learning_logs:topic', topic_id=topic_id)
            
    context = {'topic': topic, 'form':form} #создаем форму
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    #редактируем определённую запись
    entry = Entry.objects.get(id=entry_id)
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
           
           
    

    
