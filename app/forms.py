from django import forms

from .models import MediaType, MediaUpload


class MediaUploadForm(forms.ModelForm):
    class Meta:
        model = MediaUpload
        fields = [
            'file',
            'media_type',
            'latitude',
            'longitude',
            'province',
            'district',
        ]

    def clean_media_type(self):
        media_type = self.cleaned_data['media_type']
        if media_type not in MediaType.values:
            raise forms.ValidationError('Unsupported media type.')
        return media_type

    def clean(self):
        cleaned_data = super().clean()
        latitude = cleaned_data.get('latitude')
        longitude = cleaned_data.get('longitude')

        if latitude is not None and not (-90 <= latitude <= 90):
            self.add_error('latitude', 'Latitude must be between -90 and 90.')
        if longitude is not None and not (-180 <= longitude <= 180):
            self.add_error('longitude', 'Longitude must be between -180 and 180.')

        return cleaned_data
