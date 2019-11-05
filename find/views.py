from django.http import HttpResponse
from ipware import get_client_ip

from find.models import User, Query, Fasta
from find.sources import Uniprot, SequenceNotFoundError, NCBI, Mirbase, MicroRNA

sources = [Uniprot, Mirbase, MicroRNA, NCBI]


def log_user(request):
    ip, is_routable = get_client_ip(request)
    user, created = User.objects.get_or_create(ip=ip)
    if not created:
        user.save()
    return user


def get_fasta(query):
    try:
        return Fasta.objects.get(accession=query)
    except Fasta.DoesNotExist:
        pass
    for source in sources:
        if source.is_valid(query):
            try:
                return source.get(query)
            except SequenceNotFoundError:
                return None


def query(request, raw_query=None):
    user = log_user(request)
    if not raw_query:
        return HttpResponse("Invalid Query")
    elif raw_query.startswith("NC_"):
        return HttpResponse("Genomes are not supported yet!")
    else:
        fasta = get_fasta(raw_query)
        query, _ = Query.objects.get_or_create(raw_query=raw_query, fasta=fasta, user=user)
        if query.fasta:
            return HttpResponse("Source:</br>{}</br></br>Fasta:</br>{}</br>{}".format(query.fasta.source, query.fasta.description.replace('>', '&gt'), query.fasta.sequence))
        else:
            return HttpResponse("No fasta found for query: {}".format(raw_query))
