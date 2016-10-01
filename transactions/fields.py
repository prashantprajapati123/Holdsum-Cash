class CurrentUserProfileDefault:
    """
    Modified version of rest_framework.fields.CurrentUserDefault to
    take account of the profile object.
    """
    def set_context(self, serializer_field):
        self.profile = serializer_field.context['request'].user.profile

    def __call__(self):
        return self.profile

    def __repr__(self):
        return 'CurrentUserProfileDefault()'
