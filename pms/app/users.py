import pandas as pd
import os
import django
from django.contrib.auth.hashers import make_password
from app.models import CustomUser  # Adjust the import according to your app name

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pms.settings')
django.setup()

def upload_users_from_excel(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)

    for index, row in df.iterrows():
        # Create a CustomUser instance
        user = CustomUser(
            username=row['username'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            email=row['email'],
            password=make_password(row['password']),  # Hash the password
            is_superuser=row.get('is_superuser', False),
            is_staff=row.get('is_staff', False),
            is_active=row.get('is_active', True),
            ippis_no=row['ippis_no'],
            usertype_id=row['usertype_id'],
            department_id=row['department_id'],
            unit_id=row['unit_id'],
            date_of_acting_appointment=row.get('date_of_acting_appointment'),
            date_of_birth=row.get('date_of_birth'),
            date_of_first_appointment=row.get('date_of_first_appointment'),
            date_of_present_appointment=row.get('date_of_present_appointment'),
            designation=row.get('designation'),
            file_number=row.get('file_number'),
            middle_name=row.get('middle_name'),
            institution=row.get('institution'),
            qualification=row.get('qualification'),
            qualification_award_date=row.get('qualification_award_date'),
            phone=row.get('phone'),
        )

        # Save the user to the database
        user.save()
        print(f"User {user.username} uploaded successfully.")

if __name__ == '__main__':
    file_path = ''  # Update with your Excel file path
    upload_users_from_excel(file_path)