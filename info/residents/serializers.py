from django.db import transaction
from rest_framework import serializers

from .models import House, Resident, Apartment, Car, ParkingSpace, Ownership


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'


class ResidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resident
        fields = ['id', 'full_name']


class HouseDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детального представления дома"""
    residents = serializers.SerializerMethodField()

    class Meta:
        model = House
        fields = ['city', 'street', 'house_number', 'residents']

    def get_residents(self, obj):
        """Метод для получения данных о жильцах дома"""
        return ResidentSerializer(obj.residents, many=True).data


class ApartmentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    number = serializers.CharField(read_only=True)
    residents_count = serializers.SerializerMethodField()

    class Meta:
        model = Apartment
        fields = ['id', 'number', 'residents_count']

    def get_residents_count(self, obj):
        return obj.ownerships.count()


class OwnershipSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    apartment = ApartmentSerializer()

    class Meta:
        model = Ownership
        fields = ['id', 'apartment', 'percentage_ownership']


class CarSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Car
        fields = ['id', 'state_number', 'brand']


class ParkingSpaceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ParkingSpace
        fields = ['id', 'location']


class ResidentDetailSerializer(serializers.ModelSerializer):
    """
     Сериализатор для детального представления жильца (Resident).
     Методы:
     - get_total_apartments: Возвращает общее количество квартир, которыми владеет жилец.
     - get_total_cars: Возвращает общее количество автомобилей, которыми владеет жилец.
     - get_total_parking_spaces: Возвращает общее количество зарезервированных парковочных мест для жильца.
     - update: Переопределенный метод для обновления данных жильца и связанных с ними объектов (квартир, автомобилей, парковочных мест).
     - destroy: Переопределенный метод для удаления жильца и всех связанных с ним объектов (квартир, автомобилей, парковочных мест).
     """
    ownerships = serializers.SerializerMethodField()
    cars = CarSerializer(many=True)
    reserved_parking_spaces = ParkingSpaceSerializer(many=True)

    total_apartments = serializers.SerializerMethodField()
    total_cars = serializers.SerializerMethodField()
    total_parking_spaces = serializers.SerializerMethodField()

    class Meta:
        model = Resident
        fields = ['full_name', 'passport_data', 'ownerships', 'total_apartments', 'cars', 'total_cars',
                  'reserved_parking_spaces',
                  'total_parking_spaces']

    def get_ownerships(self, obj):
        house_id = self.context['house_id']
        ownerships = obj.ownerships.filter(apartment__house_id=house_id)
        return OwnershipSerializer(ownerships, many=True).data

    def get_total_apartments(self, obj):
        house_id = self.context['house_id']
        return obj.ownerships.filter(apartment__house_id=house_id).count()

    def get_total_cars(self, obj):
        return obj.cars.count()

    def get_total_parking_spaces(self, obj):
        return obj.reserved_parking_spaces.count()

    def update(self, instance, validated_data):
        ownerships_data = self.initial_data.get('ownerships', [])
        cars_data = validated_data.pop('cars', [])
        parking_spaces_data = validated_data.pop('reserved_parking_spaces', [])

        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.passport_data = validated_data.get('passport_data', instance.passport_data)
        instance.save()

        with transaction.atomic():
            for ownership_data in ownerships_data:
                ownership_id = ownership_data.get('id')
                if ownership_id:
                    # Обновляем существующее владение
                    ownership_instance = Ownership.objects.get(id=ownership_id, resident=instance)
                    ownership_instance.percentage_ownership = ownership_data.get('percentage_ownership')
                    ownership_instance.save()
                else:
                    Ownership.objects.create(
                        resident=instance,
                        apartment_id=ownership_data.get('apartment')['id'],
                        percentage_ownership=ownership_data.get('percentage_ownership')
                    )

            for car_data in cars_data:
                car_id = car_data.get('id')
                if car_id:
                    car_instance = Car.objects.get(id=car_id, resident=instance)
                    car_instance.state_number = car_data.get('state_number')
                    car_instance.brand = car_data.get('brand')
                    car_instance.save()
                else:
                    Car.objects.create(
                        resident=instance,
                        state_number=car_data.get('state_number'),
                        brand=car_data.get('brand')
                    )

            for parking_space_data in parking_spaces_data:
                parking_space_id = parking_space_data.get('id')
                if parking_space_id:
                    parking_space_instance = ParkingSpace.objects.get(id=parking_space_id, reserved_for=instance)
                    parking_space_instance.location = parking_space_data.get('location')
                    parking_space_instance.save()
                else:
                    house_id = self.context.get('house_id')
                    house_instance = House.objects.get(id=house_id)
                    ParkingSpace.objects.create(
                        reserved_for=instance,
                        location=parking_space_data.get('location'),
                        house=house_instance
                    )

        return instance

    def destroy(self, instance):
        instance.ownerships.all().delete()
        instance.cars.all().delete()
        instance.parking_space.all().delete()
        instance.delete()


class OwnershipCreateSerializer(serializers.ModelSerializer):
    apartment = serializers.PrimaryKeyRelatedField(queryset=Apartment.objects.all(), required=True)
    percentage_ownership = serializers.DecimalField(max_digits=5, decimal_places=2, required=True)

    class Meta:
        model = Ownership
        fields = ['id', 'apartment', 'percentage_ownership']


class ResidentCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания нового жильца (Resident).
    Методы:
    - validate_ownerships: Проверяет, что переданы данные о владениях (квартира и процент собственности).
    Метод create переопределен для создания нового экземпляра жильца и всех связанных объектов (владений, автомобилей, парковочных мест).
    """
    ownerships = OwnershipCreateSerializer(many=True, required=True)
    cars = CarSerializer(many=True, required=False)
    reserved_parking_spaces = ParkingSpaceSerializer(many=True, required=False)

    class Meta:
        model = Resident
        fields = ['id', 'full_name', 'passport_data', 'ownerships', 'cars', 'reserved_parking_spaces']

    def validate_ownerships(self, value):
        if not value:
            raise serializers.ValidationError("The apartment number and percentage of ownership are not provided.")
        return value

    def create(self, validated_data):
        ownerships_data = validated_data.pop('ownerships', [])
        cars_data = validated_data.pop('cars', [])
        reserved_parking_spaces_data = validated_data.pop('reserved_parking_spaces', [])

        # Извлекаем house_id из контекста представления
        house_id = self.context.get('house_id')
        resident = Resident.objects.create(**validated_data)

        # Создаем владения
        for ownership_data in ownerships_data:
            apartment_data = ownership_data.pop('apartment')
            apartment_id = apartment_data.id
            apartment = Apartment.objects.get(id=apartment_id)
            Ownership.objects.create(resident=resident, apartment=apartment, **ownership_data)

        # Создаем машины, если данные переданы
        for car_data in cars_data:
            Car.objects.create(resident=resident, **car_data)

        # Создаем парковочные места, если данные переданы
        for parking_space_data in reserved_parking_spaces_data:
            house = House.objects.get(id=house_id)
            ParkingSpace.objects.create(reserved_for=resident, house=house, **parking_space_data)

        return resident
