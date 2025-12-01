
from django.core.management.base import BaseCommand
from octofit_tracker.models import Team, User, Activity, Workout, Leaderboard
from django.utils import timezone
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'


    def handle(self, *args, **options):
        # Clean collections using pymongo
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        db['activities'].delete_many({})
        db['workouts'].delete_many({})
        db['leaderboard'].delete_many({})
        db['users'].delete_many({})
        db['teams'].delete_many({})


        # Create teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create users
        users = [
            User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=marvel),
            User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel),
            User.objects.create(name='Wonder Woman', email='wonderwoman@dc.com', team=dc),
            User.objects.create(name='Batman', email='batman@dc.com', team=dc),
        ]

        # Create activities
        Activity.objects.create(user=users[0], type='Running', duration=30, date=timezone.now().date())
        Activity.objects.create(user=users[1], type='Cycling', duration=45, date=timezone.now().date())
        Activity.objects.create(user=users[2], type='Swimming', duration=60, date=timezone.now().date())
        Activity.objects.create(user=users[3], type='Yoga', duration=20, date=timezone.now().date())

        # Create workouts
        Workout.objects.create(name='Hero HIIT', description='High intensity for heroes', suggested_for='Marvel')
        Workout.objects.create(name='Power Yoga', description='Strength and flexibility', suggested_for='DC')

        # Create leaderboard
        Leaderboard.objects.create(team=marvel, points=100)
        Leaderboard.objects.create(team=dc, points=80)

        # Ensure unique index on email for users
        db['users'].create_index([('email', 1)], unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data'))
