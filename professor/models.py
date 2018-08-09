from django.db import models

class Rubric(models.Model):
    course_id = models.CharField(max_length=100, default='')
    terminal_objetive = models.CharField(max_length=500)
    activity = models.CharField(max_length=500)
    approved = models.CharField(max_length=500,  default='')
    notapproved = models.CharField(max_length=500,  default='')
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    problem_id = models.IntegerField()
    contest_id = models.IntegerField()


class Evaluation(models.Model):
    code_student = models.CharField(max_length=100)
    name_student = models.CharField(max_length=500)
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE)
    note = models.FloatField()
