import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger("apps")


class EmailService:
    @staticmethod
    def send_email(
        subject,
        recipient_list,
        template_name,
        context=None,
        from_email=None,
        cc=None,
        bcc=None,
        fail_silently=False,
        attachments=None,
    ):
        """
        Отправляет email с HTML и текстовой версиями.

        Args:
            subject (str): Тема письма.
            recipient_list (list): Список получателей.
            template_name (str): Путь к шаблону письма.
            context (dict, optional): Контекст для рендеринга шаблона. По умолчанию пустой словарь.
            from_email (str, optional): Адрес отправителя. По умолчанию берется из настроек.
            cc (list, optional): Список адресов для копии.
            bcc (list, optional): Список адресов для скрытой копии.
            fail_silently (bool): Если True, ошибки отправки игнорируются.
            attachments (list, optional): Список вложений в формате [(filename, content, mimetype), ...].

        Raises:
            ValueError: Если входные данные некорректны.
            RuntimeError: Если отправка не удалась и fail_silently=False.
        """
        try:
            from_email = from_email or getattr(settings, "EMAIL_HOST_USER", None)
            if not from_email:
                raise ValueError(_("EMAIL_HOST_USER must be set in settings"))

            html_message = render_to_string(template_name, context)
            plain_message = strip_tags(html_message)

            email = EmailMultiAlternatives(
                subject=subject,
                body=plain_message,
                from_email=from_email,
                to=recipient_list,
                cc=cc or [],
                bcc=bcc or [],
            )
            email.attach_alternative(html_message, "text/html")

            if attachments:
                for filename, content, mimetype in attachments:
                    email.attach(filename, content, mimetype)

            email.send(fail_silently=fail_silently)
            logger.info(f"Email sent to {recipient_list} with subject '{subject}'")

        except FileNotFoundError as e:
            error_msg = _(f"Template '{template_name}' not found: {str(e)}")
            logger.error(error_msg)
            if not fail_silently:
                raise RuntimeError(error_msg)

        except Exception as e:
            error_msg = _(f"Failed to send email: {str(e)}")
            logger.error(error_msg)
            if not fail_silently:
                raise RuntimeError(error_msg)

    @classmethod
    def send_invitation_email(cls, invitation):
        """
        Отправляет приглашение на регистрацию.

        Args:
            invitation: Объект Invitation с полями email, get_invitation_url() и group.
        """
        subject = _("Your Registration Invitation")
        recipient_list = [invitation.email]
        template_name = "account/invitation_send.html"
        context = {
            "invitation_url": f"{settings.DOMAIN}{invitation.get_invitation_url()}",
            "group": invitation.group.name,
        }

        logger.info(f"Sending invitation email to {invitation.email}")

        cls.send_email(subject, recipient_list, template_name, context)
