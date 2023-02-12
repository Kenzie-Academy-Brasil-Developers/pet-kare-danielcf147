# Generated by Django 4.1.6 on 2023-02-10 02:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("groups", "0002_remove_group_pet"),
        ("pets", "0003_alter_pet_group"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pet",
            name="group",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pets",
                to="groups.group",
            ),
        ),
    ]
