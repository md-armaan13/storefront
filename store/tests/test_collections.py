
from rest_framework.test import APIClient
# import status_code
from rest_framework import status
import pytest
from model_bakery import baker as Baker
from store.models import Collection

# THIS FIXTURE IS SPECIFIC TO THIS TEST FILE
# RETURN THE API CALL FUNCTION
@pytest.fixture
# we cant not take parameteras value because a it consider it as a fixture
def get_api_call():
    # so we return the fuction with required parameters
    # we are taking client as argument beacuse some client ar authenticated and some are not
    def do_api_call(data, client):
        return client.post('/store/collections/', data=data)
    return do_api_call


@pytest.mark.django_db  # this decorator will create a new database for testing
class TestcreateCollection:
    def test_if_user_is_anonymous_returns_401(self, get_client, get_api_call):

       # AAA (Arrange, Act, Assert)
        # Arrange

        # Act
        response = get_api_call(data={
            "title": "test collection",
        }, client=get_client)
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Authenticating user

    def test_if_user_is_authenticated_but_not_admin_returns_403(self, get_authenticated_client, get_api_call):

        # AAA (Arrange, Act, Assert)

        # Arrange
        client = get_authenticated_client(is_staff=False)

        # Act
        response = get_api_call(data={
            "title": "test collection",
        }, client=client)

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # user is authenticated and IsAdmin but data is invalid

    def test_if_user_is_admin_but_data_is_invalid_returns_400(self, get_authenticated_client, get_api_call):

        client = get_authenticated_client(is_staff=True)

        response = get_api_call(data={
            "title": "",
        }, client=client)

        # Assert
        assert response.data['title'] == ['This field may not be blank.']
        assert response.data['title'] is not None  # explain this line

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_admin_and_data_is_valid_returns_201(self, get_authenticated_client, get_api_call):

        # Arrange
        client = get_authenticated_client(is_staff=True)

        # Act
        response = get_api_call(data={
            "title": "hello world",
        }, client=client)

        # Assert
        assert response.data['title'] != ['This field may not be blank.']
        assert response.data['title'] is not None  # explain this line
        assert response.data['id'] > 0
        assert response.status_code == status.HTTP_201_CREATED




@pytest.mark.django_db
class TestRetreiveCollection:

    def test_if_collection_does_not_exist_returns_404(self, get_client):
        # Arrange
        
        # Act
        response = get_client.get('/store/collections/1/')
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_collection_exist_returns_200(self, get_client):
        # Arrange
        collection = Baker.make(Collection)
        print(collection.__dict__)
        # Act
        response = get_client.get(f'/store/collections/{collection.id}/')
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": collection.id,
            "title": collection.title,
            "products_count_sample": 0,
        }

    def test_if_particular_collection_exist_returns_200(self, get_client):
        
        collection = Baker.make(Collection)
        
        response= get_client.get(f'/store/collections/{collection.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data is not None
        assert response.data == {
            "id": collection.id,
            "title": collection.title,
            "products_count_sample": 0,
        }

@pytest.mark.django_db
class TestUpdatingCollection :

    def test_if_user_is_anonymous_returns_401(self, get_client):
        # Arrange
        collection = Baker.make(Collection)
        # Act
        response = get_client.put(f'/store/collections/{collection.id}/', data={
            "title": "updated title",
        })
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_but_not_admin_returns_403(self, get_authenticated_client):
        # Arrange
        client = get_authenticated_client(is_staff=False)
        collection = Baker.make(Collection)
        # Act
        response = client.put(f'/store/collections/{collection.id}/', data={
            "title": "updated title",
        })
        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_but_data_is_invalid_returns_400(self, get_authenticated_client):
        # Arrange
        client = get_authenticated_client(is_staff=True)
        collection = Baker.make(Collection)
        # Act
        response = client.put(f'/store/collections/{collection.id}/', data={
            "title": "    ",
        })
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] == ['This field may not be blank.']

    def test_if_user_is_admin_and_data_is_valid_returns_200(self, get_authenticated_client):

        client = get_authenticated_client(is_staff=True)
        collection = Baker.make(Collection)

        response = client.put(f'/store/collections/{collection.id}/', data={
            "title": "updated title",
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == "updated title"
        assert response.data['title'] != collection.title
        assert response.data['id'] == collection.id
