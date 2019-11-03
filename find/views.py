from django.http import HttpResponse
from ipware import get_client_ip

from find.models import User, Query, Fasta
from find.sources import Uniprot

sources = [Uniprot]


def log_user(request):
    ip, is_routable = get_client_ip(request)
    user, created = User.objects.get_or_create(ip=ip)
    if not created:
        user.save()
    return user


def get_fasta(query):
    # TODO: Implement
    for source in sources:
        if source.is_valid(query):
            fasta_tuple = source.get(query)
            fasta, _ = Fasta.objects.get_or_create(**fasta_tuple._asdict())
            return fasta


def query(request, raw_query=None):
    user = log_user(request)
    if not raw_query:
        return HttpResponse("Invalid Query")
    else:
        fasta = get_fasta(raw_query)
        query, _ = Query.objects.get_or_create(raw_query=raw_query, fasta=fasta, user=user)
        return HttpResponse("{}\n{}".format(query.fasta.description, query.fasta.sequence))
