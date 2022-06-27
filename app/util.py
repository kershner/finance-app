from django.utils import timezone
import json
import os


def get_parameters():
    # Load params from JSON file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(base_dir + '/parameters.json') as f:
        params = json.load(f)
        return params


def get_user():
    from .models import CustomUser
    try:
        return CustomUser.objects.get(id=1)
    except CustomUser.DoesNotExist:
        return None


def setup_db_first_time():
    from .models import CustomUser, TransactionGroup

    # Create some initial transaction groups
    TransactionGroup.objects.create(group_type='in', group_name='Employment')
    TransactionGroup.objects.create(group_type='ex', group_name='Housing')
    TransactionGroup.objects.create(group_type='ex', group_name='Utility')
    TransactionGroup.objects.create(group_type='ex', group_name='Food')
    TransactionGroup.objects.create(group_type='ex', group_name='Investment')

    # Create dummy user on first startup
    user = CustomUser.objects.create(
        username='new_user',
        first_name='First Name',
        last_name='Last Name',
        birth_date=timezone.now(),
        starting_value=0,
        is_staff=True,
        is_superuser=True,
        is_active=True
    )
    user.set_password('admin')
    user.save()

    return user
