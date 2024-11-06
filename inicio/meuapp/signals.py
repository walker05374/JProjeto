from googleapiclient.discovery import build
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


GOOGLE_API_KEY = 'AIzaSyDzn1gNy0Zjh2JRwULVJ-ZtC9a9r9VHwsw'
GOOGLE_CSE_ID = '47069417be7bc44e8'

def google_custom_search(query):
    service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
    result = service.cse().list(q=query, cx=GOOGLE_CSE_ID).execute()
    return result.get('items', [])


class AppTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.pk) + text_type(timestamp))


account_activation_token = AppTokenGenerator()



