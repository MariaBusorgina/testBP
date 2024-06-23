from django.core.exceptions import ValidationError
from django.db import models


class House(models.Model):
    """Модель для описания дома"""
    city = models.CharField(max_length=100, verbose_name='город')
    street = models.CharField(max_length=150, verbose_name='улица')
    house_number = models.CharField(max_length=10, verbose_name='номер')

    def __str__(self):
        return f"г.{self.city}, ул.{self.street}, {self.house_number}"


class Resident(models.Model):
    """Модель для описания жильца"""
    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    passport_data = models.CharField(max_length=50, verbose_name='паспорт')

    def __str__(self):
        return self.full_name


class Apartment(models.Model):
    """Модель для описания квартиры"""
    number = models.CharField(max_length=10, unique=True, verbose_name='номер')
    house = models.ForeignKey(House, related_name='apartments', on_delete=models.CASCADE, verbose_name='дом')

    def __str__(self):
        return f'Квартира №{self.number}'

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Проверяем, изменилось ли поле number
            original = Apartment.objects.get(pk=self.pk)
            if original.number != self.number:
                raise ValidationError("Номер квартиры нельзя изменить")
        super().save(*args, **kwargs)


class Ownership(models.Model):
    """Модель, представляющая долю владения жильца в квартире"""
    apartment = models.ForeignKey(Apartment, related_name='ownerships', on_delete=models.CASCADE,
                                  verbose_name='номер квартиры')
    resident = models.ForeignKey(Resident, related_name='ownerships', on_delete=models.CASCADE,
                                 verbose_name='владелец квартиры')
    percentage_ownership = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='процент собственности')


class Car(models.Model):
    """Модель, представляющая данные об автомобиле, зарегистрированном на жильца"""
    state_number = models.CharField(max_length=20, verbose_name='гос.номер')
    brand = models.CharField(max_length=50, verbose_name='марка')
    resident = models.ForeignKey(Resident, related_name='cars', on_delete=models.CASCADE, verbose_name='владелец')


class ParkingSpace(models.Model):
    """Модель, представляющая парковочное место, закрепленное за жильцом"""
    location = models.CharField(max_length=100, verbose_name='место')
    house = models.ForeignKey(House, related_name='parking_space', on_delete=models.CASCADE, verbose_name='дом')
    reserved_for = models.ForeignKey(Resident, related_name='reserved_parking_spaces', on_delete=models.CASCADE,
                                     verbose_name='владелец')
