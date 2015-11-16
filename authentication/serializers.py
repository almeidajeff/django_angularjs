# -*- coding:utf-8 -*-
from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from authentication.models import Account

# Classe para serializar (JSON) os dados do usuário
class AccountSerializer(serializers.ModelSerializer):
    # o campo de senha não será incluindo na váriavel fields, pois é necessário \
    # passar o parametro required=False.
    # cada campo será obrigatório menos o campo de senha
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    # A sub classe Meta define quais metadados requeridos serão serializados 
    class Meta:
        # Como a class AccountSerializer é herança de serializers.ModelSerializer, é necessário \
        # dizer qual é o modelo que deve ser serializado.  Especificando o modelo cria uma garantia \
        # de que só os atributos desse modelo ou campos criados explicitamente podem ser serializados.
        model = Account

        # Definição dos campos serializados
        fields = ('id', 'email', 'username', 'created_at', 'updated_at',
                  'first_name', 'last_name', 'tagline', 'password',
                  'confirm_password',)
        read_only_fields = ('created_at', 'updated_at',)

        def create(self, validated_data):
            # Transforma JSON em um objeto Python. Isto é chamado deserialização e é tratado pelo método .create() \
            # Ao criar um novo objeto, como uma Conta, .create() é usado. Quando mais tarde atualizar essa conta, .update() será usado.
            return Account.objects.create(**validated_data)

        def update(self, instance, validated_data):
            # O usuário pode atualizar seu username e sua tagline. |
            # Se estas chaves estão presentes no dicionário arrays, vamos usar o novo valor. \
            # Caso contrário, o valor atual do objeto instânciado será usado.
            instance.username = validated_data.get('username', instance.username)
            instance.tagline = validated_data.get('tagline', instance.tagline)

            instance.save()

            password = validated_data.get('password', None)
            confirm_password = validated_data.get('confirm_password', None)

            # Checando se o que foi digitado no campo senha é igual ao que foi digitado no campo confirmar senha.
            if password and confirm_password and password == confirm_password:
                instance.set_password(password)
                instance.save()

            update_session_auth_hash(self.context.get('request'), instance)

            return instance