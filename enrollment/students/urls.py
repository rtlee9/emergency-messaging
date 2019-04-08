from django.urls import path

from enrollment.students import views

app_name = 'students'
urlpatterns = [
    path('students/', view=views.StudentListView.as_view(), name='student-list'),
    path('students/<int:pk>/', view=views.StudentDetailView.as_view(), name='student-detail'),
    path('students/add/', views.StudentCreate.as_view(), name='student-add'),
    path('students/<int:pk>/update/', views.StudentUpdate.as_view(), name='student-update'),
    path('students/<int:pk>/delete/', views.StudentDelete.as_view(), name='student-delete'),
    path('addresses/', view=views.AddressListView.as_view(), name='address-list'),
    path('addresses/<int:pk>/', view=views.AddressDetailView.as_view(), name='address-detail'),
    path('addresses/add/', views.AddressCreate.as_view(), name='address-add'),
    path('addresses/<int:pk>/update/', views.AddressUpdate.as_view(), name='address-update'),
    path('addresses/<int:pk>/delete/', views.AddressDelete.as_view(), name='address-delete'),
    path('parents/', view=views.ParentListView.as_view(), name='parent-list'),
    path('parents/<int:pk>/', view=views.ParentDetailView.as_view(), name='parent-detail'),
    path('parents/add/', views.ParentCreate.as_view(), name='parent-add'),
    path('parents/<int:pk>/update/', views.ParentUpdate.as_view(), name='parent-update'),
    path('parents/<int:pk>/delete/', views.ParentDelete.as_view(), name='parent-delete'),
    path('sms', views.sms_response)
]
