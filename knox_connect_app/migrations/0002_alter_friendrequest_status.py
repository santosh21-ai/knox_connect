# Generated by Django 5.1.1 on 2024-09-08 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knox_connect_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendrequest',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Reject', 'Reject')], default='Not set', max_length=20),
        ),
    ]
