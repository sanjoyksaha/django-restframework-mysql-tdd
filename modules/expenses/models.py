from django.db import models

# Create your models here.
class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)
    details = models.TextField()
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        db_table = "expense_categories"

    def __str__(self):
        return self.name