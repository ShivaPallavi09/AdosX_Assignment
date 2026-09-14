import csv
import os
from django.core.management.base import BaseCommand
from reconciler.models import Location, SystemARecord, SystemBRecord

class Command(BaseCommand):
    help = 'Imports raw data from CSV files into the database without dropping dirty rows.'

    def handle(self, *args, **kwargs):
        # Resolve the path to the root 'data' directory
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        data_dir = os.path.join(base_dir, 'data')

        self.stdout.write("Clearing existing data...")
        Location.objects.all().delete()
        SystemARecord.objects.all().delete()
        SystemBRecord.objects.all().delete()

        loc_path = os.path.join(data_dir, 'locations.csv')
        if os.path.exists(loc_path):
            with open(loc_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                locations = [
                    Location(
                        location_id=row.get('location_id', '').strip(),
                        org_id=row.get('org_id', '').strip()
                    ) for row in reader
                ]
                Location.objects.bulk_create(locations)
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded locations.'))
        else:
            self.stdout.write(self.style.WARNING(f'locations.csv not found at {loc_path}'))

        sys_a_path = os.path.join(data_dir, 'system_a.csv')
        if os.path.exists(sys_a_path):
            with open(sys_a_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                sys_a_records = [
                    SystemARecord(
                        record_id=row.get('record_id', '').strip(),
                        value=row.get('value', '').strip(),
                        location_id=row.get('location_id', '').strip()
                    ) for row in reader
                ]
                SystemARecord.objects.bulk_create(sys_a_records)
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded System A records.'))
        else:
            self.stdout.write(self.style.WARNING(f'system_a.csv not found.'))

        sys_b_path = os.path.join(data_dir, 'system_b.csv')
        if os.path.exists(sys_b_path):
            with open(sys_b_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                sys_b_records = [
                    SystemBRecord(
                        record_ref=row.get('record_ref', '').strip(),
                        value=row.get('value', '').strip(),
                        location_id=row.get('location_id', '').strip()
                    ) for row in reader
                ]
                SystemBRecord.objects.bulk_create(sys_b_records)
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded System B records.'))
        else:
            self.stdout.write(self.style.WARNING(f'system_b.csv not found.'))