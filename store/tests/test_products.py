
from rest_framework.test import APIClient
# import status_code
from rest_framework import status
import pytest
from model_bakery import baker as Baker
from store.models import Collection ,Product ,Cart

# THIS FIXTURE IS SPECIFIC TO THIS TEST FILE
# RETURN THE API CALL FUNCTION
@pytest.fixture
# we cant not take parameteras value because a it consider it as a fixture
def get_api_call():
    # so we return the fuction with required parameters
    # we are taking client as argument beacuse some client ar authenticated and some are not
    def do_api_call(data, client):
        return client.post('/store/products/', data=data)
    return do_api_call

@pytest.mark.django_db  # this decorator will create a new database for testing
class TestCreateProduct :

    def test_if_user_is_anonymous_returns_401(self, get_client, get_api_call):

        

        response = get_api_call(data ={
            "title": "Nimbuu",
            "price_of_product": 45,
            "inventory":  90,
            "collection":  3,
            "description" : "nice PRoduct",
        }, client=get_client)
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_but_not_admin_return_403(self, get_authenticated_client, get_api_call):

        client = get_authenticated_client(is_staff=False)

        response = get_api_call(data ={
            "title": "Nimbuu",
            "price_of_product": 45,
            "inventory":  90,
            "collection":  3,
            "description" : "nice PRoduct",
        }, client=client)
        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_but_data_is_invalid_returns_400(self, get_authenticated_client, get_api_call):
            
            client = get_authenticated_client(is_staff=True)
    
            response = get_api_call(data ={
                "title": "kii",
                "price_of_product": 45,
                "inventory":  -90,
                "collection":  3,
                "description" : "nice PRoduct",
            }, client=client)
            # Assert
            assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_admin_and_data_is_valid_returns_201(self, get_authenticated_client, get_api_call):
         
            client = get_authenticated_client(is_staff=True)
            collection = Baker.make(Collection)
            response = get_api_call(data ={
                "title": "Nimbuu",
                "price_of_product": 45,
                "inventory":  90,
                "collection":  collection.id,
                "description" : "nice PRoduct",
            }, client=client)
            # Assert
            assert response.status_code == status.HTTP_201_CREATED
