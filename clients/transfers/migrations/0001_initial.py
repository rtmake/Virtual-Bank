# Generated by Django 4.2.7 on 2023-12-12 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('transactions', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='transfer', to='transactions.transaction')),
                ('transaction_partner_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction_partner_transfers', to='accounts.account')),
            ],
        ),
    ]