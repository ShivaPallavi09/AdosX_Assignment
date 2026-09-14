from django.db import models

class Location(models.Model):
    location_id = models.CharField(max_length=255, unique=True)
    org_id = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.location_id} -> {self.org_id}"

class SystemARecord(models.Model):
    record_id = models.CharField(max_length=255)
    value = models.CharField(max_length=255, null=True, blank=True)
    location_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.record_id

class SystemBRecord(models.Model):
    record_ref = models.CharField(max_length=255)
    value = models.CharField(max_length=255, null=True, blank=True)
    location_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.record_ref