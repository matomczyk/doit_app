from django.db import migrations, models


def populate_categories(apps, schema_editor):
    Category = apps.get_model("doit_app", "Category")
    categories = ['Housing', 'Transportation', 'Groceries', 'Utilities', 'Clothing', 'Healthcare', 'Supplies',
                  'Personal', 'Education', 'Entertainment', 'Other']
    description = ['mortgage, rent, repairs', 'car payments, gas, tickets', 'groceries',
                   'electricity, water, phone, internet', 'clothing, shoes, accessories',
                   'primary care, dental care, medications, speciality care',
                   'toiletries, laundry/dishwasher detergents, tools', 'gym membership, cosmetics, salon services',
                   'school supplies, college payments, books, courses',
                   'bars, clubs, movies, concerts, vacations, subscriptions', 'other',
                   ]
    for counter in range(10):
        c = Category.objects.create(name=f'{categories[counter]}', description=f'{description[counter]}')
        c.save()

class Migration(migrations.Migration):
    dependencies = [
        ('doit_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_categories),
    ]