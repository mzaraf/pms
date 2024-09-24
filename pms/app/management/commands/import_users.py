# yourproject/yourapp/management/commands/import_users.py
import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import CustomUser  # Update with your actual model import

class Command(BaseCommand):
    help = 'Import users from Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to Excel file')

    def handle(self, *args, **options):
        file_path = options['file_path']

        try:
            df = pd.read_excel(file_path)

            for _, row in df.iterrows():
                ippis_no = row['ippis_no']
                phone_no = str(row['phone_no'])  # Convert to string if needed

                if CustomUser.objects.filter(ippis_no=ippis_no).exists() or CustomUser.objects.filter(phone_no=phone_no).exists():
                    raise ValueError(f"Duplicate user found with IPPIS No: {ippis_no} or Phone No: {phone_no}")

                user_data = {
                    'ippis_no': ippis_no,
                    'phone_no': phone_no,
                    'usertype_id': row['usertype_id'],
                    'department_id': row['department_id'],
                    'unit_id': row['unit_id'],
                    'password': row['password'],  # Add password field in your Excel file
                }
                CustomUser.objects.create_user(**user_data)

                self.stdout.write(self.style.SUCCESS(f"User {user_data['ippis_no']} created successfully."))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {e}"))