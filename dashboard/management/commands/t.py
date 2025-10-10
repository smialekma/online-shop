from django.core.management.base import BaseCommand

# from icecream import ic
# from customers.factories import CustomerFactory
from customer_addresses.factories import CustomerAddress

"""
{'_state': <django.db.models.base.ModelState object at 0x00000170C1E14530>,
'id': None,
'customer_id': None, 'first_name': 'Magdalena', 'last_name': 'Śmiałek', 'address_line': 'k[oj;pj', 'telephone': '604884059', 'postal_code': '01-708', 'city': 'Warszawa', 'country': 'Polska'}
k[oj;pj

"""


class Command(BaseCommand):
    def handle(self, *args, **options):
        # customers = CustomerFactory.create_batch(10)

        # address = CustomerAddressFactory.create()
        new_address = {
            "customer_id": None,
            "first_name": "Magdalena",
            "last_name": "Śmiałek",
            "telephone": "604884059",
            "postal_code": "01-710",
            "city": "Warszawa",
            "country": "Polska",
            "address_line": "k[oj;pj",
        }
        address_line = "k[oj;pj"
        # customer = CustomerFactory(address=address)
        new_address, created = CustomerAddress.objects.update_or_create(
            defaults=new_address, address_line=address_line
        )

        print(created)

        pass
