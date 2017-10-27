from recommends.providers import RecommendationProvider
from recommends.providers import recommendation_registry
from recommends.algorithms.pyrecsys import RecSysAlgorithm
from authentication.models import Profile
from .models import Music, Vote


class MusicRecommendationProvider(RecommendationProvider):

    def get_users(self):
        return Profile.objects.filter(is_active=True, votes__isnull=False).distinct()

    def get_items(self):
        return Music.objects.all()

    def get_ratings(self, obj):
        return Vote.objects.filter(music=obj)

    def get_rating_score(self, rating):
        return rating.score

    def get_rating_user(self, rating):
        return rating.user

    def get_rating_site(self, rating):
        return rating.site

    def get_rating_item(self, rating):
        return rating.music

recommendation_registry.register(Vote, [Music], MusicRecommendationProvider)