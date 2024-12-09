from rest_framework import serializers
from .models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = '__all__'


class CreateBorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ['book', 'expected_return_date']

    def validate(self, data):
        if data['book'].inventory <= 0:
            raise serializers.ValidationError("Book not available")
        return data

    def create(self, validated_data):
        book = validated_data['book']
        book.inventory -= 1
        book.save()
        borrowing = Borrowing.objects.create(**validated_data, user=self.context['request'].user)
        return borrowing
