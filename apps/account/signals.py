from django.db.models.signals import m2m_changed, post_migrate
from django.dispatch import receiver

from apps.account.choices import RoleChoices
from apps.account.models import Role


@receiver(m2m_changed, sender=Role.permissions.through)
def update_user_permissions(sender, instance, action, **kwargs):
    """
    Автоматически обновляет права всех пользователей с данной ролью,
    когда изменяются permissions в Role.
    """
    if action in [
        "post_add",
        "post_remove",
        "post_clear",
    ]:  # Когда добавляются/удаляются права
        print(f"🔄 Обновляем права для пользователей с ролью: {instance.name}")

        for user in instance.users.all():
            user.user_permissions.clear()  # Очистка старых прав
            user.user_permissions.add(*instance.permissions.all())  # Добавление новых прав
            print(f"✅ Обновлены права для пользователя: {user.email}")


@receiver(post_migrate)
def create_roles(sender, **kwargs):
    if sender.name == "apps.account":
        roles = [RoleChoices.ADMIN, RoleChoices.MODERATOR, RoleChoices.USER]

        existing_roles = set(Role.objects.values_list("name", flat=True))  # Получаем существующие роли

        for role in roles:
            if role not in existing_roles:
                Role.objects.create(name=role)
                print(f"✅ Created role: {role}")
            else:
                print(f"⚠️ Role already exists: {role}")
