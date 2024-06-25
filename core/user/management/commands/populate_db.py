from django.core.management import call_command
from django.core.management.base import BaseCommand
from user.models import Publisher,Commenter

class Command(BaseCommand):
    help = 'Create initial Publisher and Commenter data'

    def handle(self, *args, **kwargs):
        # Run migrations
        call_command("makemigrations")
        call_command("migrate")

        # Create Publisher objects
        admin = Publisher.objects.create_superuser(
            email='rahul@123gmail.com',
            username='rahul',
            password='rahul',
            website_url = "http://127.0.0.1:8000/posts/"
        )
        publisher1 = Publisher.objects.create_superuser(
            email='publisher1@example.com',
            username='Publisher1',
            last_name='One',
            password='password1',
            website_url = "http://127.0.0.1:8000/posts/"
        )
        publisher2 = Publisher.objects.create_superuser(
            email='publisher2@example.com',
            username='Publisher2',
            last_name='Two',
            password='password2',
            website_url = "http://127.0.0.1:8000/posts/"
        )

        # Create Commenter objects
        commenter1 = Commenter.objects.create(
            email='commenter1@example.com',
            username='Commenters3',
            last_name='One',
            password='password3'
        )
        commenter2 = Commenter.objects.create(
            email='commenter2@example.com',
            username='Commenter4',
            last_name='Two',
            password='password4'
        )

