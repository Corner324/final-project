import factory
from faker import Faker
from pytest_factoryboy import register
from app.orgstructure.models import OrganizationalUnit


class OrganizationalUnitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrganizationalUnit
