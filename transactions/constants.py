from model_utils import Choices


LOAN_STATES = Choices(
    ('rejected', 'rejected'),
    ('pending', 'pending'),
    ('awaiting_transfer', 'awaiting_transfer'),
    ('in_repayment', 'in_repayment'),
    ('paid_in_full', 'paid_in_full'),
)

PLAID_STATES = Choices(
    ('failed', 'Failed'),
    ('no_token', 'User Not Connected'),
    ('pending', 'Pending'),
    ('success', 'Success'),
)

MAXIMUM_INSUFFICENT_SCORE = -15
