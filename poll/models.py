from django.core.validators import MinValueValidator
from django.db import models

from .constants import OPINION_POLL_OPTIONS, GENDER


class IFrameEnabledSites(models.Model):
    domain = models.CharField(max_length=100, unique=True, db_index=True)
    enabled = models.BooleanField(default=False)

    def __str__(self):
        return "IFrame for site {} enabled: {}".format(self.domain, self.enabled)


class StateUnion(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Constituency(models.Model):
    state_union = models.ForeignKey(StateUnion, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class OpinionPoll(models.Model):
    email = models.EmailField(max_length=100, unique=True, blank=False, null=False, db_index=True)
    choices = models.CharField(max_length=1, choices=OPINION_POLL_OPTIONS, blank=False, null=False)
    age = models.PositiveSmallIntegerField(blank=False, validators=[MinValueValidator(18)])
    gender = models.CharField(max_length=1, choices=GENDER, blank=False, null=False)
    state = models.ForeignKey(StateUnion, on_delete=models.SET_NULL, blank=False, null=True)
    place = models.ForeignKey(Constituency, on_delete=models.SET_NULL, blank=False, null=True)
    ip_address = models.GenericIPAddressField()
    added_time = models.DateTimeField(auto_now_add=True)
