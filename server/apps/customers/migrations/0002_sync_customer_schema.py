
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Update Django's migration state without dropping
        # columns that are already absent from MySQL.
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.RemoveField(
                    model_name='customer',
                    name='email',
                ),
                migrations.RemoveField(
                    model_name='customer',
                    name='phone_number',
                ),
                migrations.AddField(
                    model_name='customer',
                    name='user',
                    field=models.OneToOneField(
                        null=True,
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='customer_profile',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
