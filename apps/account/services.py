from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _


class EmailService:
    @staticmethod
    def send_email(
        subject,
        recipient_list,
        template_name,
        context,
        from_email=None,
        fail_silently=False,
    ):
        """
        Отправляет email с HTML и текстовой версиями.

        Args:
            subject (str): Тема письма.
            recipient_list (list): Список получателей.
            template_name (str): Путь к шаблону письма.
            context (dict): Контекст для рендеринга шаблона.
            from_email (str, optional): Адрес отправителя. По умолчанию берется из настроек.
            fail_silently (bool): Если True, ошибки отправки игнорируются.
        """
        try:
            # Устанавливаем отправителя
            from_email = from_email or settings.EMAIL_HOST_USER
            if not from_email:
                raise ValueError(_("EMAIL_HOST_USER must be set in settings."))

            # Рендерим HTML-версию письма
            html_message = render_to_string(template_name, context)
            # Создаем текстовую версию, убирая HTML-теги
            plain_message = strip_tags(html_message)

            # Создаем объект письма
            email = EmailMultiAlternatives(
                subject=subject,
                body=plain_message,
                from_email=from_email,
                to=recipient_list,
            )
            # Прикрепляем HTML-версию
            email.attach_alternative(html_message, "text/html")

            # Отправляем письмо
            email.send(fail_silently=fail_silently)
        except Exception as e:
            if not fail_silently:
                raise RuntimeError(_(f"Failed to send email: {str(e)}"))
