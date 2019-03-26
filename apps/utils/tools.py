import abc
import requests
import tempfile
import os
from django.core.files import File



class GetRemoteImage:

    def __init__(self, obj):
        self.obj = obj

    def load(self):
        self._get_image()

    def _get_image(self):
        resp = requests.get(url=self.obj.external_url, stream=True)
        if resp.status_code == requests.codes.ok:
            file_name = self.obj.external_url.split('/')[-1]

            # Create a temporary file
            lf = tempfile.NamedTemporaryFile()

            # Read the streamed image in sections
            for block in resp.iter_content(1024 * 8):

                # If no more file then stop
                if not block:
                    break

                # Write image block to temporary file
                lf.write(block)

            # Save the temporary image to the model#
            # This saves the model so be sure that is it valid
            self.obj.image.save(file_name, File(lf), save=False)
            self.obj.status = self.obj.LOADED
            self.obj.save()
        elif resp.status_code == requests.codes.not_found:
            self.obj.status = self.obj.NOT_FOUND
            self.obj.save()
