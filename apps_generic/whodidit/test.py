from abc import ABC, abstractmethod

import pytest


class AbstractUserAuth(ABC):
    @abstractmethod
    def default_user(self, *args, **kwargs):
        """Base implementation for creating a default user."""

    @abstractmethod
    def authenticate_user(self, *args, **kwargs):
        """Base implementation for authenticating a user."""


class BaseUserAuth(AbstractUserAuth):
    username = 'Test User name'
    first_name = 'Test First NAME'
    last_name = 'Test Last Name'
    password = 'QW12W23333jjg'

    @pytest.fixture
    def default_user(self, django_user_model):
        user = django_user_model.objects.create_user(
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            password=self.password
        )
        user.set_password('pass5678')
        user.save()
        return user

    @pytest.fixture
    def authenticate_user(self, client, default_user):
        client.force_login(default_user)
        return default_user
