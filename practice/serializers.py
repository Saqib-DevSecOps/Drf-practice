from django.db.backends.base import validation
from rest_framework import serializers

from practice.models import Student, Song, Singer


# class StudentSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField(max_length=200)
#     email = serializers.EmailField(max_length=200)
#     age = serializers.IntegerField()


# # or
#
def start_with_s(value):
    if value[0] != 's':
        raise serializers.ValidationError('Name Must Start with s')


class StudentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200, validators=[start_with_s])
    email = serializers.EmailField(max_length=200)
    age = serializers.IntegerField()

    def create(self, validated_data):
        return Student.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.age = validated_data.get('age', instance.age)
        instance.save()
        return instance

    def validate_age(self, value):
        if value < 18:
            raise serializers.ValidationError('age is low')
        return value

    def validate(self, data):
        name = data.get('name')
        email = data.get('email')
        if len(name) <= 5:
            raise serializers.ValidationError('enter more than 5 character in name')
        if len(email) <= 5:
            raise serializers.ValidationError('enter more than 5 character in name')
        return data


class SongSerializer(serializers.ModelSerializer):
    # singer = serializers.StringRelatedField(many=True,read_only=True)
    # singer = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    singer = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='singer-detail')


# singer = serializers.SlugRelatedField(many=True,read_only=True,slug_field='name')
# singer = serializers.HyperlinkedIdentityField(view_name='singer-detail')

    class Meta:
        model = Song
        fields = ['id', 'title', 'duration', 'singer']


# class SingerSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Singer
#         fields = ['id', 'name', 'song']

class SingerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Singer
        fields = ['id', 'song', 'name', ]
