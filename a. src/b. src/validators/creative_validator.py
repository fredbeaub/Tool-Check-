import os
from PIL import Image
import magic
from moviepy.editor import VideoFileClip

class CreativeValidator:
    def __init__(self, file, ad_type):
        self.file = file
        self.ad_type = ad_type
        self.specs = self._get_specs()

    def validate(self):
        # Sauvegarde temporaire du fichier
        temp_path = os.path.join('uploads', self.file.filename)
        self.file.save(temp_path)

        try:
            # Déterminer le type de fichier
            file_type = magic.from_file(temp_path, mime=True)
            
            if 'image' in file_type:
                return self._validate_image(temp_path)
            elif 'video' in file_type:
                return self._validate_video(temp_path)
            else:
                return {'valid': False, 'errors': ['Invalid file type']}
        finally:
            # Nettoyage
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def _validate_image(self, file_path):
        errors = []
        try:
            with Image.open(file_path) as img:
                # Vérifier le format
                if img.format.lower() not in self.specs['image']['formats']:
                    errors.append(f"Invalid format: {img.format}")

                # Vérifier la taille du fichier
                if os.path.getsize(file_path) > self.specs['image']['max_file_size']:
                    errors.append("File size exceeds maximum allowed")

                # Vérifier les dimensions
                width, height = img.size
                if (width, height) not in self.specs['image']['dimensions'].values():
                    errors.append(f"Invalid dimensions: {width}x{height}")

        except Exception as e:
            errors.append(f"Error processing image: {str(e)}")

        return {
            'valid': len(errors) == 0,
            'errors': errors
        }

    def _validate_video(self, file_path):
        errors = []
        try:
            with VideoFileClip(file_path) as clip:
                # Vérifier la durée
                if clip.duration > self.specs['video']['max_duration']:
                    errors.append("Video duration exceeds maximum allowed")

                # Vérifier les dimensions
                width, height = clip.size
                if width < self.specs['video']['min_resolution'][0] or \
                   height < self.specs['video']['min_resolution'][1]:
                    errors.append("Video resolution too low")

        except Exception as e:
            errors.append(f"Error processing video: {str(e)}")

        return {
            'valid': len(errors) == 0,
            'errors': errors
        }

    def _get_specs(self):
        # Spécifications selon le type d'annonce
        return {
            'streaming_tv': {
                'video': {
                    'formats': ['mp4'],
                    'max_duration': 180,
                    'min_resolution': (1920, 1080)
                }
            },
            'display': {
                'image': {
                    'formats': ['jpg', 'png'],
                    'max_file_size': 2 * 1024 * 1024,
                    'dimensions': {
                        'medium_rectangle': (300, 250),
                        'leaderboard': (728, 90)
                    }
                }
            }
        }[self.ad_type]
