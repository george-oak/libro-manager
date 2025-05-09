from rest_framework import serializers


class BookBuySerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
