from django.urls import path, include
from home import views
from .views import UserLoginView

urlpatterns = [
    path('',views.index,name='home'),
    path('login',UserLoginView.as_view(),name='login'),
    path('logout',views.logout_view,name='logout'),
    path('update_task/<task_id>',views.update_task,name='update-task'),
    path('delete_task/<task_id>',views.delete_task,name='delete-task'),
]
