from django.core.management.base import BaseCommand
from django.conf import settings
import redis
from images.models import Image

class Command(BaseCommand):
    help = 'Update the image ranking in Redis'

    def handle(self, *args, **options):
        # Connect to Redis
        r = redis.StrictRedis(host=settings.REDIS_HOST, 
                              port=settings.REDIS_PORT, 
                              db=settings.REDIS_DB)
        
        # Get the current ranking from Redis
        image_ranking = r.zrange('image_ranking', 0, -1)
        image_ranking_ids = [int(id) for id in image_ranking]

        # Get IDs of existing images from the database
        existing_image_ids = list(Image.objects.values_list('id', flat=True))

        # Remove IDs from Redis that are no longer in the database
        for image_id in image_ranking_ids:
            if image_id not in existing_image_ids:
                r.zrem('image_ranking', image_id)

        self.stdout.write(self.style.SUCCESS('Successfully updated image ranking in Redis'))
