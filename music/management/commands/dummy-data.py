import random
import names
import datetime
from model_mommy import mommy
from django.core.management.base import BaseCommand
from music.models import Music, Genre


class Command(BaseCommand):
    help = "My shiny new management command."

    def add_arguments(self, parser):
        parser.add_argument('count', nargs='+', type=int)

    def handle(self, *args, **options):
        print('Hello world')

        self.cleardatabase()
        self.make_genres()
        self.make_musics(options)

    def cleardatabase(self):
        Music.objects.all().delete()
        Genre.objects.all().delete()

    def make_genres(self):
        genre_names = (
            'Pop', 'Jazz', 'Rock', 'Folk', 'Blues', 'Hip hop', 'Country', 'Classic', 'Rap', 'Disco', 'Electro'
        )
        self.genres = []
        for name in genre_names:
            g = mommy.make(Genre, genre_name=name)
            self.genres.append(g)

    def make_musics(self, options):
        self.musics = []
        for _ in range(options.get('count')[0]):
            m = mommy.prepare(
                Music,
                name=names.get_first_name(),
                genre=random.choice(self.genres),
                links='https://www.youtube.com/watch?v=YQHsXMglC9A',
                artist=names.get_full_name(),
                release_date=datetime.date.today()
            )
            self.musics.append(m)
        Music.objects.bulk_create(self.musics)

    def connect_musics(self):

        stud_courses = []
        for student_id in Student.objects.values_list('pk', flat=True):
            courses_already_linked = []
            for _ in range(random.randint(1, 10)):
                index = random.randint(0, len(self.courses) - 1)
                if index not in courses_already_linked:
                    courses_already_linked.append(index)
                else:
                    continue
                stud_courses.append(
                    ThroughModel(
                        student_id=student_id,
                        course_id=self.courses[index].pk
                    )
                )
        ThroughModel.objects.bulk_create(stud_courses)