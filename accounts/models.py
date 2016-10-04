from django.db import models
from django.contrib.auth.models import User

from fernet_fields import EncryptedCharField
from localflavor.us.models import USStateField, USZipCodeField
from model_utils import Choices


STATUS_CHOICES = Choices(
    ('pending', 'Pending Approval'),
    ('approved', 'Approved'),
    ('denied', 'Denied'),
)


EMPLOYMENT_CHOICES = Choices(
    ('unemployed', 'Unemployed'),
    ('selfemployed', 'Self Employed'),
    ('fulltime', 'Full Time'),
    ('parttime', 'Part Time'),
    ('student', 'Student'),
)
EMPLOYED = (EMPLOYMENT_CHOICES.fulltime, EMPLOYMENT_CHOICES.parttime)


GENDER_CHOICES = Choices(
    ('m', 'Male'),
    ('f', 'Female'),
)


PAY_FREQUENCY_CHOICES = Choices(
    ('monthly', 'Monthly'),
    ('every_two_weeks', 'Every Two Weeks'),
    ('bi_weekly', 'Bi-Weekly'),
    ('bi_monthly', 'Bi-Monthly'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.CharField(max_length=10, choices=GENDER_CHOICES)

    address = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    state = USStateField()
    zip_code = USZipCodeField()

    license = models.FileField(upload_to='licenses/', blank=True, null=True)
    paystubs = models.FileField(upload_to='paystubs/', blank=True, null=True)
    employment_status = models.CharField(max_length=30, choices=EMPLOYMENT_CHOICES,
                                         default=EMPLOYMENT_CHOICES.unemployed)

    plaid_public_token = EncryptedCharField(max_length=200, blank=True)
    plaid_access_token = EncryptedCharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default=STATUS_CHOICES.pending)

    def __str__(self):
        return '{user.first_name}, {user.last_name}'.format(user=self.user)


class Employment(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    employer_name = models.CharField(max_length=150)
    city = models.CharField(max_length=20)
    state = USStateField()
    zip_code = USZipCodeField()

    def __str__(self):
        return 'Employment for %s' % str(self.profile)
