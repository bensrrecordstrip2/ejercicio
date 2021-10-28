from django.urls import path
from .views import register,login, AuthenticateUser,logout, PermissionAPIView,RoleViewSet


#rutas a nuestras vistas 
urlpatterns = [
    #path('users/', users),
    path('register/',register),
    path('login/',login),
    path('user/',AuthenticateUser.as_view()),
    path('logout/',logout),
    path('permissions/',PermissionAPIView.as_view()),
    path('roles/',RoleViewSet.as_view({
        'get':'list',
        'post':'create',
    })),
    path('role/<str:pk>', RoleViewSet.as_view({
        'get': 'retrieve',
        'put': 'updated',
        'delete': 'destroy',
    })),
]
