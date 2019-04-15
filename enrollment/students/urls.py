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
    path('classrooms/', view=views.ClassroomListView.as_view(), name='classroom-list'),
    path('classrooms/<int:pk>/', view=views.ClassroomDetailView.as_view(), name='classroom-detail'),
    path('classrooms/add/', views.ClassroomCreate.as_view(), name='classroom-add'),
    path('classrooms/<int:pk>/update/', views.ClassroomUpdate.as_view(), name='classroom-update'),
    path('classrooms/<int:pk>/delete/', views.ClassroomDelete.as_view(), name='classroom-delete'),
    path('sites/', view=views.SiteListView.as_view(), name='site-list'),
    path('sites/<int:pk>/', view=views.SiteDetailView.as_view(), name='site-detail'),
    path('sites/add/', views.SiteCreate.as_view(), name='site-add'),
    path('sites/<int:pk>/update/', views.SiteUpdate.as_view(), name='site-update'),
    path('sites/<int:pk>/delete/', views.SiteDelete.as_view(), name='site-delete'),
]
