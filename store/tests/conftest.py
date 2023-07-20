import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User

# RETURN THE APICLIENT OBJECT
@pytest.fixture
def get_client():
    return APIClient()


@pytest.fixture
def get_authenticated_client(get_client):# USING API CLIENT FIXTURE TO GET API CLIENT OBJECT
    #RETURNINING A FUNCTION THAT TAKES IS_STAFF AS A PARAMETER
    def do_authentication(is_staff=False):
        get_client.force_authenticate(user=User(is_staff=is_staff))
        return  get_client
    
    return do_authentication