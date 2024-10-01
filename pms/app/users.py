import pandas as pd
import os
import django
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from app.models import CustomUser, Department, Unit, Usertype  # Adjust the import according to your app name

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pms.settings')
django.setup()

def send_login_details(first_name, email, ippis_no, password):
    subject = "NASRDA PMS: Login Credentials"
    message = f'Dear {first_name},\n\nYour account has been created successfully on the NASRDA PMS. Below are your login details:\n\n'
    f'IPPIS Number: your ippis number\n'
    f'Password: {password}\n'
    f'Link: pe.nasrda.gov.ng\n\n'
    f'Please change your password after your first login.\n\n'
    f'Thank you.',
    from_email = os.getenv('DEFAULT_FROM_EMAIL')  # Use the email from your settings
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    print(f"Email sent to {email}.")

def upload_users_from_excel(file_path):
    try:
        # Read the Excel file
        df = pd.read_excel(file_path)

        for index, row in df.iterrows():
            try:
                # Check if a user with the same ippis_no already exists
                if CustomUser.objects.filter(ippis_no=row['ippis_no']).exists():
                    print(f"User with IPPIS number {row['ippis_no']} already exists. Skipping.")
                    continue

                # Retrieve foreign key relationships if necessary
                department = Department.objects.get(id=row['department_id'])
                unit = Unit.objects.get(id=row['unit_id'])
                usertype = Usertype.objects.get(id=row['usertype_id'])

                # Generate raw password for email
                raw_password = row['password']

                # Create a CustomUser instance
                user = CustomUser(
                    username=row['username'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    email=row['email'],
                    password=make_password(raw_password),  # Hash the password
                    is_superuser=row.get('is_superuser', False),
                    is_staff=row.get('is_staff', False),
                    is_active=row.get('is_active', True),
                    ippis_no=row['ippis_no'],
                    usertype=usertype,
                    department=department,
                    unit=unit,
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

                # Send login details via email
                send_login_details(user.email, user.ippis_no, raw_password)

            except Department.DoesNotExist:
                print(f"Department with id {row['department_id']} not found.")
            except Unit.DoesNotExist:
                print(f"Unit with id {row['unit_id']} not found.")
            except Usertype.DoesNotExist:
                print(f"Usertype with id {row['usertype_id']} not found.")
            except Exception as e:
                print(f"Error processing row {index + 1}: {str(e)}")

    except Exception as e:
        print(f"Error reading the Excel file: {str(e)}")

if __name__ == '__main__':
    file_path = 'path_to_your_excel_file.xlsx'  # Update with your Excel file path
    upload_users_from_excel(file_path)