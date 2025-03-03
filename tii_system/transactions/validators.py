from django.core.exceptions import ValidationError
from django.conf import settings
from django.template.defaultfilters import filesizeformat

def validate_file_size(content):
    # Get File Attribute
    filesize    = content.size
    ext         = content.name.split('.')[-1]

    # Check File Extention
    if ext.lower() in settings.CONTENT_TYPES:

        # Check File Size
        if filesize > int(settings.MAX_UPLOAD_SIZE):
            raise ValidationError((f'Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(filesize)))
    else:
        raise ValidationError((f'File type is not supported. The supported file are .PDF .DOC .DOCX'))
    return content
