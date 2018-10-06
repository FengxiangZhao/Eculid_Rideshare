import re

# A Case ID pattern, recoginizes lower-case alphanumeric in the form <Three letter><1-9999>
CASE_ID_PATTERN = re.compile(r"^[a-z]{3}((?!0))[0-9]{1,4}$")
# A list contains all recognized case email domain
# Currently, since CWRU offers alias, only should <case id>@case.edu should be allowed
CASE_EMAIL_DOMAIN = ["case.edu",]

# Usage: CASE_ID_PATTERN.match(case_id)

########################################################

# emails
EUCLID_CARSHARE_MAIL_ADDRESS = "euclid.carshare@gmail.com"
EUCLID_CARSHARE_MAIL_PASSWORD = "sherlock8"

#TODO::
def send_verification_email(address, token):
    '''
    Send an verification email to the specified address that contains the verification link
    Args:
        address: the recipient of the verification email
        token: the link token that relates the recipient
            a link will be generated under our domain that contains the token
            in the form sample.url.com?verify_token=<token>
    Returns: True if the email is delivered, false otherwise
    '''
    return False

#TODO::
def get_verification_token():
    '''
    obtain a verification token.
    Returns: a alphanumeric token
    '''

    return "ab1234"