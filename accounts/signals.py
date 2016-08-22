from .yodlee import yodlee


def on_create_link_yodlee(created=False, instance=None, **kwargs):
    if not created:
        return

    yodlee.register3(instance)
