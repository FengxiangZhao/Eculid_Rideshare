# django
from django.core import mail
from django.test import TestCase
from django.test.utils import override_settings
from django.template.loader import render_to_string
# rest_framework
from rest_framework.test import APIClient
# local
from euclid_userauth.models import Client
from tests.utils import generate_random_user_info, get_status_code_error_msg

# use debug mode to let non-case email pass through
@override_settings(DEBUG=True)
class GetClientInformationTest(TestCase):

    def setUp(self):
        self.target_url = "http://testserver/account/"
        self.user_info = generate_random_user_info()

    def test_anonymous_user(self):
        '''
        Anonymous client could not obtain their information
        Expecting status code 401 Unauthorized
        '''
        response = APIClient().get(self.target_url)

        expected_status_code = 401
        self.assertEqual(
            response.status_code,
            expected_status_code,
            get_status_code_error_msg(expected_status_code, response.status_code)
        )

    def test_registered_user(self):

        req = APIClient()
        client_obj = Client.objects.create_user(**self.user_info)
        req.force_authenticate(user=client_obj)
        response = req.get(self.target_url)

        expected_status_code = 200
        self.assertEqual(
            response.status_code,
            expected_status_code,
            get_status_code_error_msg(expected_status_code, response.status_code)
        )

        # password is not returned in the response data
        del self.user_info["password"]
        for key in self.user_info.keys():
            self.assertEqual(
                self.user_info[key],
                response.data[key],
                "Response data mismatch at {:s}".format(key)
            )


@override_settings(
    DEBUG=True, # use debug mode to let non-case email pass through
    EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend' # use memery email backend to avoid email actuall got sent
)
class ClientRegistrationTest(TestCase):

    def setUp(self):
        self.target_url = "http://testserver/account/register/"

    def register_random(self):
        randominfo = generate_random_user_info()
        return self.register(randominfo)

    def register(self, info):
        cli = APIClient()
        response = cli.post(self.target_url, data=info, format='json')
        return info, response


    def test_normal_registration(self):
        '''
        A normal registration should return status code of 201 and
        the json returned should be the same as information supplied.
        '''
        clientinfo, response = self.register_random()

        expected_status_code = 201
        self.assertEqual(
            response.status_code,
            expected_status_code,
            get_status_code_error_msg(expected_status_code, response.status_code)
        )

        self.assertDictEqual(
            response.data,
            clientinfo,
            'Wrong registration info'
        )

        # should receive and email
        self.assertEqual(
            len(mail.outbox),
            1,
            "Email Verification is not sent？"
        )

        self.assertTrue(
            render_to_string(
                "api/email_verification_subject.txt",
                context=clientinfo
            ) in \
            mail.outbox[0].subject,
            "Email subject wrong"
        )

    def test_repeat_registration(self):
        '''
        The client information such as email, phone and username should be unique
        '''
        clientinfo, response = self.register_random()
        expected_status_code = 201
        self.assertEqual(
            response.status_code,
            expected_status_code,
            get_status_code_error_msg(expected_status_code, response.status_code)
        )

        _, response = self.register(clientinfo)

        expected_status_code = 400
        self.assertEqual(
            response.status_code,
            expected_status_code,
            get_status_code_error_msg(expected_status_code, response.status_code)
        )

        for k in response.data.keys():
            self.assertEqual(
                response.data[k][0].code,
                "unique"
            )






