# Generated by Django 4.2.4 on 2023-09-22 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("beautician", "0022_otp"),
    ]

    operations = [
        migrations.AddField(
            model_name="otp",
            name="email",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
