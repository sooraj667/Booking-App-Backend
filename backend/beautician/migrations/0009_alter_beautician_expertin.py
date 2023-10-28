# Generated by Django 4.2.4 on 2023-09-10 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("beautician", "0008_beautician_expertin_alter_beautician_services"),
    ]

    operations = [
        migrations.AlterField(
            model_name="beautician",
            name="expertin",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="beauticians_expert_in",
                to="beautician.services",
            ),
        ),
    ]
