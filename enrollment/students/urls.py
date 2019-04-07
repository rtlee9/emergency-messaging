from django.urls import path

from enrollment.students import views

app_name = 'students'
urlpatterns = [
    path('', view=views.StudentListView.as_view(), name='student-list'),
    path('<int:pk>/', view=views.StudentDetailView.as_view(), name='student-detail'),
    path('add/', views.StudentCreate.as_view(), name='student-add'),
    path('<int:pk>/update/', views.StudentUpdate.as_view(), name='student-update'),
    path('<int:pk>/delete/', views.StudentDelete.as_view(), name='student-delete'),
]
