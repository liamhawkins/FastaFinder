from django.db import models


class Query(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    raw_query = models.CharField(max_length=50)
    fasta_source = models.ForeignKey("FastaSource", null=True, blank=True, on_delete=models.DO_NOTHING)
    user = models.ForeignKey("User", related_name="user_queries", on_delete=models.DO_NOTHING)


class FastaSource(models.Model):
    accession = models.CharField(max_length=20, primary_key=True)
    url = models.CharField(max_length=255)
    source = models.CharField(max_length=20)


class User(models.Model):
    first_time_queried = models.DateTimeField(auto_now_add=True)
    most_recent_time_queried = models.DateTimeField(auto_now=True)
    num_queries = models.PositiveIntegerField(default=1)
    ip = models.GenericIPAddressField(blank=True, null=True)


class MicroRNAAlias(models.Model):
    alias = models.CharField(max_length=25, primary_key=True)
    accession = models.CharField(max_length=15)
