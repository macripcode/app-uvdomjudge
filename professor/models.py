from django.db import models

class Rubric(models.Model):
    terminal_objetive = models.CharField(max_length=500)
    activity = models.CharField(max_length=500)
    weight = models.PositiveIntegerField()
    problem_id = models.IntegerField()
    contest_id = models.IntegerField()


class Evaluation(models.Model):
    code_student = models.CharField(max_length=100)
    name_student = models.CharField(max_length=500)
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE)
    note = models.FloatField()