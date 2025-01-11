from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from nxtbn.filemanager.models import Image, Document


from PIL import Image as PILImage
from io import BytesIO
from django.core.files.base import ContentFile

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_by",
            "last_modified_by",
        )

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["created_by"] = request.user
        validated_data["last_modified_by"] = request.user

        # Optimize the image before saving
        if "image" in validated_data:
            validated_data["image"] = self.optimize_image(validated_data["image"])
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context["request"]
        validated_data["last_modified_by"] = request.user

        # Optimize the image if it is being updated
        if "image" in validated_data:
            validated_data["image"] = self.optimize_image(validated_data["image"])
        
        return super().update(instance, validated_data)

    @staticmethod
    def optimize_image(image_file, max_size_kb=200, format="WEBP"):
        """
        Optimize an image by resizing and converting it to the specified format while maintaining the aspect ratio.
        Ensures the image file size is below max_size_kb.
        """
        img = PILImage.open(image_file)
        img = img.convert("RGB")  # Ensure compatibility for formats like PNG with alpha

        # Resize the image to fit within a reasonable dimension (adjust if needed)
        max_dimension = 800
        img.thumbnail((max_dimension, max_dimension), PILImage.Resampling.LANCZOS)

        # Save the image to a buffer
        buffer = BytesIO()
        img.save(buffer, format=format, optimize=True, quality=85)
        buffer.seek(0)

        # Check if the image exceeds the maximum size, reduce quality iteratively
        while buffer.tell() > max_size_kb * 1024:
            buffer.seek(0)
            img.save(buffer, format=format, optimize=True, quality=max(10, 85 - 10))
            buffer.seek(0)

        # Return the new image as a ContentFile
        return ContentFile(buffer.read(), name=f"{image_file.name.split('.')[0]}.{format.lower()}")




class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_by",
            "last_modified_by",
        )

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["last_modified_by"] = self.context["request"].user
        return super().create(validated_data)
