# Generated by Django 4.2.4 on 2023-10-13 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("beautician", "0023_otp_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="beautician",
            name="wallet_amount",
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
    ]
