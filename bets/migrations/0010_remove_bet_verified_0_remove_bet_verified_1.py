# Generated by Django 4.2.16 on 2024-09-27 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bets", "0009_alter_transaction_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bet",
            name="verified_0",
        ),
        migrations.RemoveField(
            model_name="bet",
            name="verified_1",
        ),
    ]