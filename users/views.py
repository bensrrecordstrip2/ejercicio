from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from rest_framework import exceptions, viewsets, status
from .serializers import UserSerializer, PermissionSerializer,RoleSerializer
from .authentication import generate_access_token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .authentication import JWTAuthentication

#Registramos un usuario
@api_view(['POST'])
def register(request):
    data = request.data
    if data['password'] != data['password_confirm']:
        raise exceptions.APIException('Password no son iguales')

    serializer = UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

#hacemos el logueo de un usuario con su correo y password
@api_view(['POST'])
def login(request):
    email= request.data.get('email')
    password = request.data.get('password')

    user = User.objects.filter(email=email).first()
    #validacion si no encuentra a un usuario
    if user is None:
        raise exceptions.AuthenticationFailed('user not found')
    #validacion si la contraseña es incorrecta
    if not user.check_password(password):
        raise exceptions.AuthenticationFailed('Incorrect Password')

    response = Response()
    #Genera el token para que pueda navegar el usuario
    token = generate_access_token(user)
    #para acceder a la vista en front
    response.set_cookie(key='jwt',value=token,httponly=True)
    response.data ={
        'jwt':token
    }
    return response




#borra la cookie y hace logout del token
@api_view(['POST'])
def logout(request):
    response= Response()
    response.delete_cookie(key='jwt')
    response.data ={
    'message':'success'
    }

    return response

# da informacion acerca del usuario que se autentico
class AuthenticateUser(APIView):
    autentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({
            'data': serializer.data
        })



# obtención de todos los usuarios
#@api_view(['GET'])
#def users(request):
    #serializer =UserSerializer(User.objects.all(),many=True)
    #return Response(serializer.data)


# esta clase hace que cuando tengamos el token podamos entrar y tener los permisos para editar modificar o consultar dependiento el usuario
class PermissionAPIView(APIView):
    autentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = PermissionSerializer(Permission.objects.all(), many=True)
        return Response({
            'data': serializer.data
        })


## es una clase para ver los roles y tambien agregar es un crud de roles con sus metodos
class RoleViewSet(viewsets.ViewSet):
    autentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        serializer = RoleSerializer(Role.objects.all(), many=True)
        return Response({
            'data':serializer.data
        })

    def create(self, request):
        serializer = RoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response({
            'data':serializer.data
        }, status= status.HTTP_201_CREATED)


    def retrieve(self, request, pk=None):
        pass

    def update(self, request,pk=None):
        pass

    def destroy(self, request,pk=None):
        pass
