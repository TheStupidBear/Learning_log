from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

# def user_logout(request):
# 	#выход из авторизации
# 	logout(request)
# 	return redirect('logout')

def register(request):
	#регистрация нового пользователя
	if request.method != 'POST':
		#выводит пустую форму регистрации 
		form = UserCreationForm()
	else:
		#обработка заполненной формы
		form = UserCreationForm(data=request.POST)
		if form.is_valid():
			new_user = form.save()
			#выполнение входа и перенаправление на домашнюю страницу
			login(request, new_user)
			return redirect('learning_logs:index')
	#вывести пустую или недействительную форму
	context = {'form': form}
	return render(request, 'registration/register.html', context)