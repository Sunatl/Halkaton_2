# Generated by Django 5.0 on 2024-12-19 10:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_customuser_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='grade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='api.grade'),
        ),
    ]
