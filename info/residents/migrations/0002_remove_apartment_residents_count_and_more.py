# Generated by Django 5.0.6 on 2024-06-22 20:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('residents', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apartment',
            name='residents_count',
        ),
        migrations.AlterField(
            model_name='apartment',
            name='house',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apartments', to='residents.house', verbose_name='дом'),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='number',
            field=models.CharField(max_length=10, verbose_name='номер'),
        ),
        migrations.AlterField(
            model_name='car',
            name='brand',
            field=models.CharField(max_length=50, verbose_name='марка'),
        ),
        migrations.AlterField(
            model_name='car',
            name='resident',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars', to='residents.resident', verbose_name='владелец'),
        ),
        migrations.AlterField(
            model_name='car',
            name='state_number',
            field=models.CharField(max_length=20, verbose_name='гос.номер'),
        ),
        migrations.AlterField(
            model_name='house',
            name='city',
            field=models.CharField(max_length=100, verbose_name='город'),
        ),
        migrations.AlterField(
            model_name='house',
            name='house_number',
            field=models.CharField(max_length=10, verbose_name='номер'),
        ),
        migrations.AlterField(
            model_name='house',
            name='street',
            field=models.CharField(max_length=150, verbose_name='улица'),
        ),
        migrations.AlterField(
            model_name='ownership',
            name='apartment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ownerships', to='residents.apartment', verbose_name='номер квартиры'),
        ),
        migrations.AlterField(
            model_name='ownership',
            name='percentage_ownership',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='процент собственности'),
        ),
        migrations.AlterField(
            model_name='ownership',
            name='resident',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ownerships', to='residents.resident', verbose_name='владелец квартиры'),
        ),
        migrations.AlterField(
            model_name='parkingspace',
            name='house',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parking_space', to='residents.house', verbose_name='дом'),
        ),
        migrations.AlterField(
            model_name='parkingspace',
            name='location',
            field=models.CharField(max_length=100, verbose_name='место'),
        ),
        migrations.AlterField(
            model_name='parkingspace',
            name='reserved_for',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reserved_parking_spaces', to='residents.resident', verbose_name='владелец'),
        ),
        migrations.AlterField(
            model_name='resident',
            name='full_name',
            field=models.CharField(max_length=255, verbose_name='ФИО'),
        ),
        migrations.AlterField(
            model_name='resident',
            name='passport_data',
            field=models.CharField(max_length=50, verbose_name='паспорт'),
        ),
    ]
