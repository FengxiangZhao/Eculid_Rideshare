import random
import string

def generate_random_string(N):
    '''
    generate random lowercase alphanumeric string of length N
    '''
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(N))


def generate_random_phone():
    '''
    generate random number of length 10 in place of a U.S. phone number
    '''
    return ''.join(random.choice(string.digits) for _ in range(10))

def generate_random_user_info():
    return {
        "username" : generate_random_string(5),
        "email" : generate_random_string(8) + '@gmail.com',
        "password" : generate_random_string(8),
        "phone" : generate_random_phone()
    }


def get_status_code_error_msg(expected, actual):
    return "Expected Status Code: {:d} \n Actual Status Code : {:d}".format(expected, actual)