from rest_framework import serializers

from finance.models import Plan, PlanAttribute


class PlanAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanAttribute
        fields = ('plan', 'name')


class PlanSerializer(serializers.ModelSerializer):
    attributes = serializers.SerializerMethodField(method_name='get_plan_attributes', read_only=True)
    price = serializers.SerializerMethodField(method_name='get_price', read_only=True)

    class Meta:
        model = Plan
        exclude = ('is_active', 'created', 'modified')

    def get_plan_attributes(self, obj):
        attributes = obj.attributes.all()
        return PlanAttributeSerializer(instance=attributes, many=True).data

    def get_price(self, obj):
        return obj.get_price()
