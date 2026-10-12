from rest_framework import serializers


class CategorySerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    details = serializers.CharField(required=False, allow_blank=True, allow_null=True, default="")
    status = serializers.IntegerField(min_value=0, max_value=1)
    created_at = serializers.DateTimeField(required=False, allow_null=True)
    updated_at = serializers.DateTimeField(required=False, allow_null=True)
    deleted_at = serializers.DateTimeField(required=False, allow_null=True)