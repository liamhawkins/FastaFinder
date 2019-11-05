from django.db import models


class Query(models.Model):
    first_time_queried = models.DateTimeField(auto_now_add=True)
    most_recent_time_queried = models.DateTimeField(auto_now=True)
    raw_query = models.CharField(max_length=50)
    fasta = models.ForeignKey("Fasta", null=True, blank=True, on_delete=models.DO_NOTHING)
    user = models.ForeignKey("User", related_name="user_queries", on_delete=models.DO_NOTHING)


class Fasta(models.Model):
    accession = models.CharField(max_length=20, primary_key=True)
    description = models.CharField(max_length=255)
    sequence = models.TextField()
    source = models.CharField(max_length=255)


class User(models.Model):
    first_time_queried = models.DateTimeField(auto_now_add=True)
    most_recent_time_queried = models.DateTimeField(auto_now=True)
    ip = models.GenericIPAddressField(blank=True, null=True)


class MicroRNAAlias(models.Model):
    alias = models.CharField(max_length=25, primary_key=True)
    accession = models.CharField(max_length=15)
