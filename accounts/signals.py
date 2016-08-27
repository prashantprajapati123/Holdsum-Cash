from .yodlee import yodlee, gen_password


def on_create_link_yodlee(created=False, instance=None, **kwargs):
    if not created:
        return

    instance.yodleepw = gen_password()
    instance.save()
    yodlee.register3(instance)
