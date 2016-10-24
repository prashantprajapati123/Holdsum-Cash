from django.core.mail import send_mail


def on_create_notify(created=False, instance=None, **kwargs):
    if not created:
        return

    if instance.is_superuser:
        return

    send_mail('New User Created!', '', 'robot@holdsum.com', ['nick.webb04@gmail.com'])
