from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os
from django.core.files.storage import default_storage
from io import BytesIO


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='pictures', default=os.path.join('pictures', 'avatar.png'))

    def save(self, *args, **kwargs):
        # run save of parent class above to save original image to disk
        super().save(*args, **kwargs)

        memfile = BytesIO()

        img = Image.open(self.profile_pic)
        if img.height > 1000 or img.width > 1000:
            output_size = (200, 200)
            img.thumbnail(output_size, Image.ANTIALIAS)
            img.save(memfile, 'JPEG', quality=95)
            default_storage.save(self.profile_pic.name, memfile)
            memfile.close()
            img.close()
