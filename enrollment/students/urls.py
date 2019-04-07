from django.urls import path

from enrollment.students import views

app_name = 'students'
urlpatterns = [
    path('students/', view=views.StudentListView.as_view(), name='student-list'),
    path('students/<int:pk>/', view=views.StudentDetailView.as_view(), name='student-detail'),
    path('students/add/', views.StudentCreate.as_view(), name='student-add'),
    path('students/<int:pk>/update/', views.StudentUpdate.as_view(), name='student-update'),
    path('students/<int:pk>/delete/', views.StudentDelete.as_view(), name='student-delete'),
    path('parents/', view=views.ParentListView.as_view(), name='parent-list'),
    path('parents/<int:pk>/', view=views.ParentDetailView.as_view(), name='parent-detail'),
    path('parents/add/', views.ParentCreate.as_view(), name='parent-add'),
    path('parents/<int:pk>/update/', views.ParentUpdate.as_view(), name='parent-update'),
    path('parents/<int:pk>/delete/', views.ParentDelete.as_view(), name='parent-delete'),
]
