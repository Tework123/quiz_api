from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # авторизация
    path('api/v1/auth/', include('rest_framework.urls')),

    # регистрация
    path('api/v1/register/', include('register.urls')),

    path('api/v1/quiz/', include('quiz.urls'))

    # path(теперь надо странички составить с нужными ручками)


]
