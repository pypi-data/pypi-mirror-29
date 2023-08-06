from government.models import Party
from rest_framework import serializers


class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = (
            'uid',
            'slug',
            'label',
            'short_label',
            'ap_code',
        )
