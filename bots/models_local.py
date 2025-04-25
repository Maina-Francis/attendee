from django.core.files.storage import FileSystemStorage
from django.conf import settings

class LocalBotDebugScreenshotStorage(FileSystemStorage):
    """Local filesystem storage for debug screenshots in development."""
    
    def __init__(self):
        super().__init__(
            location=settings.MEDIA_ROOT,
            base_url=settings.MEDIA_URL
        ) ``