from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

MAX_SCORE = 5


class BaseReview(models.Model):
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Integer rating 1-{MAX_SCORE}"
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
     # to know if the review was updated - or edited
    # is_approved = models.BooleanField(default=True)        # first goes to staff - idk if it's a great deal... (maybe?)

    class Meta:
        abstract = True 

    def __str__(self):
        return f"{self.student} ({self.score})"

class ReviewTeacher(BaseReview):
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews_received",
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews_made",
    )

    class Meta:
        verbose_name = "Teacher Review"
        verbose_name_plural = "Teacher Reviews"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["teacher", "student"], name="unique_teacher_student_review"
            )
        ]
        indexes = [
            models.Index(fields=["teacher"]),
            models.Index(fields=["student"]),
        ]

    def __str__(self):
        return f"{self.teacher} — {self.student} ({self.score})"
        