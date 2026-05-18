from django import forms

from reviews.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "review_text", "is_recommended"]
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 10}),
            "review_text": forms.Textarea(attrs={"rows": 4}),
        }
        labels = {
            "rating": "Rating (1-10)",
            "review_text": "Your Review",
            "is_recommended": "Do you recommend this game?",
        }
