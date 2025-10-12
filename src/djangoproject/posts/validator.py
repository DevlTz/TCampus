from rest_framework.exceptions import ValidationError

def validate_image_size(image):
    max_size_mb = 10
    if image.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Very large file. Max allowed is: {max_size_mb}MB.")
    return image
