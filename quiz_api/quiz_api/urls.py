from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # авторизация для rest
    path('api/v1/auth/', include('rest_framework.urls')),
    path('api/v1/quiz/', include('quiz.urls'))

    # path(теперь надо странички составить с нужными ручками)


]
