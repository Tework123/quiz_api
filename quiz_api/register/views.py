from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from register.serializers import UserSerializer


class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # это обращение обязательно нужно,
        # здесь как раз передаются аргументы и выполняется сериализатор,
        # только надо в переменную это записать
        super().create(request, *args, **kwargs)
        return Response({
            'status': 200,
            'message': 'Register success',
        })
