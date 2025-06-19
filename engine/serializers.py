from rest_framework import serializers


class CellSerializer(serializers.Serializer):
    x = serializers.IntegerField()
    y = serializers.IntegerField()
    energy = serializers.FloatField()
    age = serializers.IntegerField()
    type = serializers.StringRelatedField(source='__class__.__name__')
    photosynthesis = serializers.FloatField(source='genome.photosynthesis')
    speed = serializers.FloatField(source='genome.speed')
    sense_distance = serializers.IntegerField(source='genome.sense_distance')
    reproduction_rate = serializers.FloatField(source='genome.reproduction_rate')
