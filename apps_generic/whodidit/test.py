from dataclasses import dataclass

import pytest


@dataclass
class UserData:
    username = 'Test User name'
    first_name = 'Test First NAME'
    last_name = 'Test Last Name'
    password = 'QW12W23333jjg'


@pytest.fixture
def default_user(django_user_model, user_data=UserData):
    user = django_user_model.objects.create_user(
        username=user_data.username,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        password=user_data.password
    )
    user.set_password('pass5678')
    user.save()
    return user


@pytest.fixture
def authenticated_user(client, default_user):
    client.force_login(default_user)
    return default_user
