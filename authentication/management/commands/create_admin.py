from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser for Django admin'

    def handle(self, *args, **options):
        try:
            # Get admin credentials from environment or use defaults
            admin_username = os.getenv('ADMIN_USERNAME', 'admin')
            admin_email = os.getenv('ADMIN_EMAIL', 'admin@recursion.com')
            admin_password = os.getenv('ADMIN_PASSWORD', 'recursion123')
            
            # Check if superuser already exists
            if User.objects.filter(username=admin_username).exists():
                self.stdout.write(
                    self.style.WARNING(f'Superuser "{admin_username}" already exists')
                )
                return
            
            # Create superuser
            User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created superuser "{admin_username}"')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'Could not create superuser: {str(e)}')
            )
            # Don't fail the deployment if superuser creation fails
            pass
