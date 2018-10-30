from django.contrib.auth.models import AbstractUser
from django.db import models

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
    ('employed', 'Employed'),
    ('unemployed', 'Unemployed'),
)


GENDER_CHOICES = Choices(
    ('m', 'Male'),
    ('f', 'Female'),
)


PAY_FREQUENCY_CHOICES = Choices(
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly'),
    ('biweekly', 'Bi-Weekly'),
)

USER_ACCESS_TYPE_CHOICES = Choices(
    ('borrower', 'Borrower'),
    ('lender', 'Lender'),
)


class User(AbstractUser):
    middle_initial = models.CharField(max_length=10, blank=True)
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
    no_of_failed_transection = models.IntegerField(null=True)
    plaid_score = models.DecimalField(max_digits=10, decimal_places=2, null=True,default=0 )
    questionnaire_score = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    repayment_score = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    access_type = models.CharField(max_length=10, choices=USER_ACCESS_TYPE_CHOICES,
                              default=USER_ACCESS_TYPE_CHOICES.borrower)


    def __str__(self):
        return '{self.first_name}, {self.last_name}'.format(self=self)

    @property
    def completed_profile(self):
        return all([self.ssn, self.sex, self.address, self.city, self.state, self.zip_code,
                    self.monthly_income, self.next_paydate, self.funds_source, self.pay_frequency,
                    self.license, self.paystubs])

    def notify(self, subject, message, **kwargs):
        self.email_user(subject, message)


class Employment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    employer_name = models.CharField(max_length=150)
    city = models.CharField(max_length=20)
    state = USStateField()
    zip_code = USZipCodeField()

    def __str__(self):
        return 'Employment for %s' % str(self.user)
