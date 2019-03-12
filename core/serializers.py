from rest_framework import serializers

from core.constants import TIMERANGE_DICT


class TimeRangeSerializer(serializers.Serializer):
    timerange = serializers.CharField(max_length=20, source="range")

    def validate_range(self, range):
        timeranges = TIMERANGE_DICT.keys()

        if not range:
            raise serializers.ValidationError("range is required")

        if isinstance(range, list):
            range = range[0]

        if range and range not in timeranges:
            raise serializers.ValidationError("This timerange is not allowed.")

        return range
