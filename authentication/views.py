# -*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework import permissions, viewsets

from authentication.models import Account
from authentication.permissions import IsAccountOwner
from authentication.serializers import AccountSerializer
# Create your views here.

# A viewset, como o nome indica, é um conjunto de set em views. \
# Especificamente, o ModelViewSet oferece uma interface para listar, criar, recuperar, atualizar e destruir \
# objetos de um determinado modelo.
class AccountViewSet(viewsets.ModelViewSet):
    # Sobreescrevendo a váriavel lookup_field que por padrão busca pelo ID do objeto, \
    # E nesse caso queremos buscar os usuários pelo atributo username.
    lookup_field = 'username'

    # O Django REST usa o queryset para efetuar buscas no Banco de Dados e retorna os valores.
    # Na queryset abaixo são retornados todos os usuários.
    queryset = Account.objects.all()

    #Serializando os dados a partir da classe criada no arquivo serializers.py
    serializer_class = AccountSerializer

    def get_permissions(self):
        # O único usuário responsável por executar os métodos como UPDATE ou DELETE será somente o usuário da prórpia conta.
        # O método get_permissions verifica se o usuário esta autenticado e atribui uma permissão temporária.
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        # Tratanto caso o método enviado pelo request seja via POST.
        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(), IsAccountOwner(),)

    def create(self, request):
        # Quando um objeto é criado usando o método do serializer .save(), os atributos do objeto são definidas literalmente. \
        # Isso significa que um usuário registra uma senha 'password' a senha será guardada como 'password'. |
        # Isso é ruim para por duas razões: 
            # 1) Armazenar senhas em texto simples é um problema de segurança enorme.
            # 2) Django cria hashes e solta as senhas antes de compará-los, de modo que o usuário não seria capaz de se logar usando 'password' como senha.

        serializer = self.serializer_class(data=request.data)

        # Verificando se os dados serializados são válidos
        if serializer.is_valid():
            Account.objects.create_user(**serializer.validated_data)

            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'A conta não pode ser criado com os dados recebidos.'
        }, status=status.HTTP_400_BAD_REQUEST)

