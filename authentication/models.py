# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
# Create your models here.

# Criando uma classe Manager para a Conta do usuário
class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('O usuário deve ter um endereço de email válido.')

        if not kwargs.get('username'):
            raise ValueError('O usuário deve ter um username válido.')

        # self.model se refere ao atributo modelo de BaseUserManager. \ 
        # Este padrão é settings.AUTH_USER_MODEL, mas será alterado no AUTH_USER_MODEL do arquivo settings.py
        account = self.model(
            email=self.normalize_email(email), username=kwargs.get('username')
        )

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)

        account.is_admin = True
        account.save()

        return account

# Criando modelo de dados para a aplicação Authentication Not Google Plus
class Account(AbstractBaseUser):
    """ Campos utilizados para criação do usuário, a classe criada
        é uma herança de AbstractBaseUser, nela serão adicionados novos campos
        como: tagline """

    # Campos iniciais
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)

    # Campos adicionais
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=150, blank=True)
    tagline = models.CharField(max_length=150, blank=True)

    # Flag usuário administrador
    is_admin = models.BooleanField(default=False)

    # Criar e atualizar usuário
    # O campo created_at regista o quando o objeto da conta foi criado. \
    # Ao passar auto_now_add = True para models.DateTimeField, \
    # estamos dizendo ao Django que este campo deve ser ajustado automaticamente quando o objeto é criado e \
    # não editável depois disso.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Para instanciar um modelo em Django, é necessário usar a expressão form Model.objects.get(**kwargs). \
    # Os objetos atribuem aqui uma classe Manager cujo nome tipicamente segue o <model name> mais Manager por convenção.
    objects = AccountManager()

    # A aplicação irá utilizar o endereço de e-mail do usuário para registrar o usuário
    USERNAME_FIELD = 'email'

    # Definição de campos obrigatórios
    REQUIRED_FIELDS = ['username']
    

    # Alterando o comportamento padrão do método __unicode__ retornar o e-mail
    def __unicode__(self):
        return self.email

    # Método para retorna nome completo
    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    # Método primeiro nome
    def get_short_name(self):
        return self.first_name

