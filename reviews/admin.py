from django.contrib import admin
from .models import Genre, Subgenre, Microgenre, Keyword, \
WebsiteMetadescriptor, Reviewer, MovieCreator, Country, \
    CreativeRole, Movie, MovieParticipation, Title, MovieFranchise, \
    MovieReview, ReferencedMovie, Grade, Contributor, Article, MovieRemake, \
    MovieInMovSeries, MovieSeries

# Register your models here.

admin.site.register(Genre)
admin.site.register(Grade)
admin.site.register(Subgenre)
admin.site.register(Microgenre)
admin.site.register(Keyword)
admin.site.register(WebsiteMetadescriptor)
admin.site.register(Reviewer)
admin.site.register(Contributor)
admin.site.register(MovieCreator)
admin.site.register(Country)
admin.site.register(CreativeRole)
admin.site.register(MovieParticipation)
admin.site.register(Title)
admin.site.register(Movie)
admin.site.register(MovieFranchise)
admin.site.register(MovieReview)
admin.site.register(ReferencedMovie)
admin.site.register(Article)
admin.site.register(MovieRemake)
admin.site.register(MovieInMovSeries)
admin.site.register(MovieSeries)