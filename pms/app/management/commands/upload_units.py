import pandas as pd
from django.core.management.base import BaseCommand
from app.models import Unit  # Replace with the actual model import
from django.db import transaction

class Command(BaseCommand):
    help = 'Creates new Unit records based on an Excel file'

    # Define the file path directly in the script
    file_path = 'C:/Users/GRID3__02/Desktop/PMS_Data/CENTRES/app_unit.xlsx'  # Update this with the actual path to your Excel file

    def handle(self, *args, **kwargs):
        # Read the Excel file using pandas
        try:
            df = pd.read_excel(self.file_path)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error reading Excel file: {str(e)}'))
            return

        # Ensure the columns 'id', 'name', and 'department_id' exist in the Excel file
        if 'id' not in df.columns or 'name' not in df.columns or 'department_id' not in df.columns:
            self.stderr.write(self.style.ERROR("Excel file must contain 'id', 'name', and 'department_id' columns"))
            return

        # Iterate through the rows and create Unit records if they don't exist
        for index, row in df.iterrows():
            unit_id = row['id']
            name = row['name']
            department_id = row['department_id']

            try:
                with transaction.atomic():
                    # Check if the unit already exists by 'id'
                    if not Unit.objects.filter(id=unit_id).exists():
                        # Create a new Unit record
                        Unit.objects.create(
                            id=unit_id,
                            name=name,
                            department_id=department_id
                        )
                        self.stdout.write(self.style.SUCCESS(f'Created new unit with id {unit_id}: {name}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Skipped creation: Unit with id {unit_id} already exists'))

            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Error occurred at row {index}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Unit creation process completed.'))

