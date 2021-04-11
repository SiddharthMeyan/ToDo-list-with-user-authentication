from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.contrib.auth.decorators import login_required
from .forms import TaskForm,CompleteTaskForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout,login
from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

class UserLoginView(LoginView):
    template_name= 'home/login.html'
    fields = '__all__'
    redirect_authenticated_user=True
    
    def get_success_url(self):
        return reverse_lazy('home')

def logout_view(request):
    logout(request)
    return redirect('/')


def register(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    form=UserCreationForm()
    return render(request,'home/register.html',{'form':form})


@login_required(login_url='login')
def index(request):
    current_user=request.user
    tasks = Task.objects.filter(user=current_user)
    form = TaskForm()
    if request.method == 'POST':
        
        form = TaskForm(request.POST or None)
        title= request.POST.get('title')
        if form.is_valid():
            user=request.user
            form=Task(user=user,title=title)
            form.save()
            return redirect('/')

    context = {'tasks':tasks, 'form':form}
    return render(request,'home/index.html',context)


@login_required(login_url='login')
def update_task(request,task_id):
    instance = get_object_or_404(Task,pk=task_id)
    user=request.user
    form = CompleteTaskForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'home/update_task.html',{'form':form, 'instance':instance,'user':user})



@login_required(login_url='login')
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    user=request.user
    if request.method == "POST":
        task.delete()
        return redirect('/')
    context = {'task':task, 'user':user}
    return render(request, 'home/delete_task.html',context)