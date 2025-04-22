import os
import sys
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils.dateparse import parse_datetime
from core.models import Admin, Category, Supplier, Item

# Setup Django environment
sys.path.append(os.path.abspath(os.path.join(__file__, *[os.pardir] * 3)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'simple_lms.settings'
import django
django.setup()

import csv
import time

start_time = time.time()

filepath = './core/db_seed/'  # Sesuaikan path jika perlu


with open(filepath + 'admins.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    obj_create = []
    for row in reader:
        if not User.objects.filter(username=row['username']).exists():
            obj_create.append(User(
                username=row['username'],
                password=make_password(row['password']),
                email=row['email'],
                is_superuser=row['is_superuser'],
                is_staff=row['is_staff']
            ))
    User.objects.bulk_create(obj_create)

print("Admin data imported successfully.")


# Import Admin data
with open(filepath + 'admins.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    obj_create = []
    for row in reader:
        if not Admin.objects.filter(username=row['username']).exists():
            obj_create.append(Admin(
                username=row['username'],
                password=make_password(row['password']),
                email=row['email'],
                created_at=parse_datetime(row['created_at']),
                updated_at=parse_datetime(row['updated_at'])
            ))
    Admin.objects.bulk_create(obj_create)

print("Model Admin data imported successfully.")

# Import Category data
with open(filepath + 'categories.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    obj_create = []
    for row in reader:
        # Pastikan created_by_id valid (ada di tabel Admin)
        if Admin.objects.filter(id=row['created_by_id']).exists():
            obj_create.append(Category(
                name=row['name'],
                description=row['description'],
                created_by_id=row['created_by_id'],
                created_at=parse_datetime(row['created_at']),
                updated_at=parse_datetime(row['updated_at'])
            ))
        else:
            print(f"Admin dengan ID {row['created_by_id']} tidak ditemukan, kategori {row['name']} dilewatkan.")
    Category.objects.bulk_create(obj_create)

print("Category data imported successfully.")

# Import Supplier data
with open(filepath + 'suppliers.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    obj_create = []
    for row in reader:
        # Pastikan created_by_id valid (ada di tabel Admin)
        if Admin.objects.filter(id=row['created_by_id']).exists():
            obj_create.append(Supplier(
                name=row['name'],
                contact_info=row['contact_info'],
                created_by_id=row['created_by_id'],
                created_at=parse_datetime(row['created_at']),
                updated_at=parse_datetime(row['updated_at'])
            ))
        else:
            print(f"Admin dengan ID {row['created_by_id']} tidak ditemukan, supplier {row['name']} dilewatkan.")
    Supplier.objects.bulk_create(obj_create)

print("Supplier data imported successfully.")

# Import Item data
with open(filepath + 'items.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    obj_create = []
    for row in reader:
        # Pastikan category_id dan supplier_id valid
        if Category.objects.filter(id=row['category_id']).exists() and Supplier.objects.filter(id=row['supplier_id']).exists():
            obj_create.append(Item(
                name=row['name'],
                description=row['description'],
                price=row['price'],
                quantity=row['quantity'],
                category_id=row['category_id'],
                supplier_id=row['supplier_id'],
                created_by_id=row['created_by_id'],
                created_at=parse_datetime(row['created_at']),
                updated_at=parse_datetime(row['updated_at'])
            ))
        else:
            print(f"Data kategori atau supplier tidak ditemukan untuk item {row['name']}, item dilewatkan.")
    Item.objects.bulk_create(obj_create)

print("Item data imported successfully.")

# Print the total time for the import process
print("--- %s seconds ---" % (time.time() - start_time))