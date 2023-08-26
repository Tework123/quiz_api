from rest_framework import permissions

from quiz.models import Quiz, Question


class IsGroup(permissions.BasePermission):
    edit_methods = ("PUT", "PATCH")

    def has_permission(self, request, view):
        user = request.user
        quiz = Quiz.objects.get(slug=request.resolver_match.kwargs["slug"])
        for group in quiz.group.all():
            if user.groups.filter(name=group.name).exists():
                return True

        # стандартная проверка
        # if request.user.is_authenticated:
        #     print('123')
        #     return True

    def has_object_permission(self, request, view, obj):

        # более избирательные проверки
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.author == request.user:
            return True

        if request.user.is_staff and request.method not in self.edit_methods:
            return True

        return False
