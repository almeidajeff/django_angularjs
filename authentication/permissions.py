from rest_framework import permissions


class IsAccountOwner(permissions.BasePermission):
	# Criando um permissão básica, de forma que se houver um usuário associado no request \
	# ser o mesmo que de um objeto Conta é retornado True, caso contrário False.
    def has_object_permission(self, request, view, account):
        if request.user:
            return account == request.user
        return False