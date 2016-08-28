from .yodlee import yodlee, get_yodlee_password


def on_create_link_yodlee(created=False, instance=None, **kwargs):
    if not created:
        return

    instance.yodleepw = get_yodlee_password()
    instance.save()
    yodlee.register3(instance)
