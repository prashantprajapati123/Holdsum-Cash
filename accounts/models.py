from django.db import models
from django.contrib.auth.models import AbstractUser

from fernet_fields import EncryptedCharField
from localflavor.us.models import USStateField, USZipCodeField
from model_utils import Choices

from .fields import EncryptedSSNField


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
    ('biweekly', 'Bi-Weekly'),
    ('bimonthly', 'Bi-Monthly'),
)


class User(AbstractUser):
    middle_initial = models.CharField(max_length=10)
    sex = models.CharField(max_length=10, choices=GENDER_CHOICES)
    ssn = EncryptedSSNField()

    address = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    state = USStateField()
    zip_code = USZipCodeField()

    monthly_income = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    next_paydate = models.DateField(null=True)
    funds_source = models.CharField(max_length=100, null=True)
    pay_frequency = models.CharField(max_length=20, choices=PAY_FREQUENCY_CHOICES)

    license = models.FileField(upload_to='licenses/', blank=True, null=True)
    paystubs = models.FileField(upload_to='paystubs/', blank=True, null=True)
    employment_status = models.CharField(max_length=30, choices=EMPLOYMENT_CHOICES)

    plaid_public_token = EncryptedCharField(max_length=200, blank=True)
    plaid_access_token = EncryptedCharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default=STATUS_CHOICES.pending)

    def __str__(self):
        return '{self.first_name}, {self.last_name}'.format(self=self)

    @property
    def completed_profile(self):
        return all([self.ssn, self.sex, self.address, self.city, self.state, self.zip_code,
                    self.monthly_income, self.next_paydate, self.funds_source, self.pay_frequency,
                    self.license, self.paystubs])


class Employment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    employer_name = models.CharField(max_length=150)
    city = models.CharField(max_length=20)
    state = USStateField()
    zip_code = USZipCodeField()

    def __str__(self):
        return 'Employment for %s' % str(self.user)
