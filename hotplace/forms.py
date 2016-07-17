from django import forms
from .models import Review


class PlaceReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ('place', 'user', 'when')

    comment = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(PlaceReviewForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False
