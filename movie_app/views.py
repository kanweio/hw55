from rest_framework.decorators import api_view
from rest_framework.response import Response
from movie_app.admin import Director, Movie, Review
from movie_app.serializer import DirectorSerializer, MovieSerializer, ReviewSerializer, MovieValidateSerializer, DirectorsValidateSerializer, ReviewValidateSerializer
from rest_framework import status


# Create your views here.
@api_view(['GET', 'POST'])
def director_view(request):
    if request.method == 'GET':
        directors = Director.objects.all()

        serializer = DirectorSerializer(directors, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = DirectorsValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        name = serializer.validated_data.get('name')
        director = Director.objects.create(name=name)
    return Response(data={'MESSAGE': 'data received!'})


@api_view(['GET', 'PUT', 'DELETE'])
def director_detail_view(request, **kwargs):
    try:
        director = Director.objects.get(id=kwargs['id'])
    except Director.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'message': 'Post not found!'})
    if request.method == 'GET':
        director = Director.objects.get(id=kwargs['id'])

        serializer = DirectorSerializer(director, many=False)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        director.name = request.data.get('title')
        return Response(data={'MESSAGE': 'data received!',
                              'director': DirectorSerializer(director).data})


@api_view(['GET', 'POST'])
def movie_view(request):
    if request.method == 'GET':
        movies = Movie.objects.all()

        serializer = MovieSerializer(movies, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        duration = serializer.validated_data.get('duration')
        director = serializer.validated_data.get('Director')
        movie = Movie.objects.create(title=title, description=description, duration=duration, director=director)
        return Response(data={'MESSAGE': 'data received!'})


@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail_view(request, **kwargs):
    try:
        movie = Movie.objects.get(id=kwargs['id'])
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'message': 'Movie not found!'})
    if request.method == 'GET':
        movie = Movie.objects.get(id=kwargs['id'])

        serializer = MovieSerializer(movie, many=False)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        movie.title = request.data.get('title')
        movie.description = request.data.get('description')
        movie.duration = request.data.get('duration')
        movie.director = request.data.get('Director')
        return Response(data={'MESSAGE': 'data received!',
                              'movie': MovieSerializer(movie).data})


@api_view(['GET', 'POST'])
def review_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()

        serializer = ReviewSerializer(reviews, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        text = serializer.validated_data.get('text')
        stars = serializer.validated_data.get('stars')
        movie = serializer.validated_data.get('movie')
        review = Review.objects.create(text=text, stars=stars, movie_id=movie)
        return Response(data={'MESSAGE': 'data received!'})


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_view(request, **kwargs):
    try:
        review = Review.objects.get(id=kwargs['id'])
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'message': 'Review not found!'})
    if request.method == 'GET':
        review = Review.objects.get(id=kwargs['id'])

        serializer = ReviewSerializer(review, many=False)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        review.text = request.data.get('text')
        review.stars = request.data.get('stars')
        review.movie_id = request.data.get('movie')
        review.save()
        return Response(data={'MESSAGE': 'data received!',
                              'review': ReviewSerializer(review).data})

