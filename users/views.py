from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from users.models import User
from users.serializers import CreateUserSerializer


class UserCreateView(CreateAPIView):
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
