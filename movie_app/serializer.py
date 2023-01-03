from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from movie_app.models import Director, Movie, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'text', 'stars', 'movie')


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(min_length=3, max_length=100)
    stars = serializers.IntegerField(min_value=1, max_value=5)
    movie_id = serializers.IntegerField()

    def validate_movie_id(self, movie_id):
        try:
            Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            raise ValidationError('Movie not found!')
        return movie_id


class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ('id', 'title', 'description', 'duration', 'director', 'reviews', 'rating')

    def get_rating(self, movie):
        stars_list = [review.stars for review in movie.reviews.all()]
        return sum(stars_list) / max(1, len(stars_list))


class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=3, max_length=100)
    description = serializers.CharField(required=False, default='No text')
    director_id = serializers.CharField()
    duration = serializers.IntegerField(min_value=40)

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError('Director not found!')
        return director_id


class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = ('id', 'name', 'movies_count')

    def get_movies_count(self, director):
        return director.movies.count()


class DirectorsValidateSerializer(serializers.Serializer):
    name = serializers.CharField()
