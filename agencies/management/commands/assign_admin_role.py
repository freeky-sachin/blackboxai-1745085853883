from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from agencies.models import UserProfile

class Command(BaseCommand):
    help = 'Assign admin role to a user by username'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the user to assign admin role')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"User '{username}' does not exist."))
            return

        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.role = 'admin'
        profile.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"UserProfile created and admin role assigned to '{username}'."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Admin role assigned to existing UserProfile of '{username}'."))
