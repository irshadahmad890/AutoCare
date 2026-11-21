from pathlib import Path
from rest_framework import serializers
from .models import RepairPhoto

class RepairPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairPhoto
        fields = ['id', 'job', 'image', 'caption', 'uploaded_by', 'created_at']
        read_only_fields = ['id', 'uploaded_by', 'created_at']

    def validate_image(self, value):
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
        allowed_types = {'image/jpeg', 'image/png', 'image/webp'}
        if Path(value.name).suffix.lower() not in allowed_extensions:
            raise serializers.ValidationError('Upload a JPG, PNG, or WEBP image.')
        if getattr(value, 'content_type', None) not in allowed_types:
            raise serializers.ValidationError('The uploaded file must be an image.')
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError('Image must be 5 MB or smaller.')
        header = value.read(12)
        value.seek(0)
        is_jpeg = header.startswith(b'\xff\xd8\xff')
        is_png = header.startswith(b'\x89PNG\r\n\x1a\n')
        is_webp = header.startswith(b'RIFF') and header[8:12] == b'WEBP'
        if not (is_jpeg or is_png or is_webp):
            raise serializers.ValidationError('The uploaded file is not a valid image.')
        return value
