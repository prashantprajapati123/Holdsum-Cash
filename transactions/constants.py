from model_utils import Choices


LOAN_STATES = Choices(
    ('rejected', 'Rejected'),
    ('pending', 'Pending'),
    ('awaiting_transfer', 'Awaiting Transfer'),
    ('in_repayment', 'In Repayment'),
    ('paid_in_full', 'Paid in Full'),
)

PLAID_STATES = Choices(
    ('failed', 'Failed'),
    ('no_token', 'User Not Connected'),
    ('pending', 'Pending'),
    ('success', 'Success'),
)

MAXIMUM_INSUFFICENT_SCORE = -15
