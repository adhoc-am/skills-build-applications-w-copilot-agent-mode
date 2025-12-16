from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models
from octofit_tracker import settings
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Clear existing data
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create teams
        marvel_team = {'name': 'Team Marvel', 'description': 'Marvel superheroes'}
        dc_team = {'name': 'Team DC', 'description': 'DC superheroes'}
        marvel_team_id = db.teams.insert_one(marvel_team).inserted_id
        dc_team_id = db.teams.insert_one(dc_team).inserted_id

        # Create users (superheroes)
        users = [
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team_id': marvel_team_id},
            {'name': 'Captain America', 'email': 'cap@marvel.com', 'team_id': marvel_team_id},
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team_id': marvel_team_id},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team_id': dc_team_id},
            {'name': 'Superman', 'email': 'superman@dc.com', 'team_id': dc_team_id},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team_id': dc_team_id},
        ]
        user_ids = db.users.insert_many(users).inserted_ids

        # Create activities
        activities = [
            {'user_id': user_ids[0], 'activity': 'Running', 'duration': 30},
            {'user_id': user_ids[1], 'activity': 'Cycling', 'duration': 45},
            {'user_id': user_ids[2], 'activity': 'Swimming', 'duration': 25},
            {'user_id': user_ids[3], 'activity': 'Running', 'duration': 40},
            {'user_id': user_ids[4], 'activity': 'Cycling', 'duration': 35},
            {'user_id': user_ids[5], 'activity': 'Swimming', 'duration': 50},
        ]
        db.activities.insert_many(activities)

        # Create leaderboard
        leaderboard = [
            {'user_id': user_ids[0], 'points': 100},
            {'user_id': user_ids[1], 'points': 90},
            {'user_id': user_ids[2], 'points': 80},
            {'user_id': user_ids[3], 'points': 110},
            {'user_id': user_ids[4], 'points': 95},
            {'user_id': user_ids[5], 'points': 85},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Create workouts
        workouts = [
            {'name': 'Morning Cardio', 'description': 'Cardio workout for all'},
            {'name': 'Strength Training', 'description': 'Strength workout for all'},
        ]
        db.workouts.insert_many(workouts)

        # Ensure unique index on email
        db.users.create_index([('email', 1)], unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
