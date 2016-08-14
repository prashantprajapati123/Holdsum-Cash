from localflavor.us.models import USSocialSecurityNumberField
from fernet_fields import EncryptedCharField


class EncryptedSSNField(EncryptedCharField, USSocialSecurityNumberField):
    pass
