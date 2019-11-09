from django.http import HttpResponse
from django.shortcuts import render
from ipware import get_client_ip

from find.models import User, Query, Fasta
from find.sources import Uniprot, SequenceNotFoundError, NCBI, Mirbase, MicroRNA

sources = [Uniprot, Mirbase, MicroRNA, NCBI]


def log_user(request):
    ip, is_routable = get_client_ip(request)
    user, created = User.objects.get_or_create(ip=ip)
    if not created:
        user.num_queries += 1
        user.save()
    return user


def get_fasta(query):
    try:
        fasta = Fasta.objects.get(accession=query)
    except Fasta.DoesNotExist:
        fasta = None
    for source in sources:
        if source.is_valid(query):
            try:
                if fasta:
                    print('returning {}.get(fasta=fasta)'.format(source.SOURCE))
                    return source.get(fasta=fasta)
                else:
                    return source.get(accession=query)
            except SequenceNotFoundError:
                return None, None, None


def query(request, raw_query=None):
    context = {
        'raw_query': raw_query,
        'fasta': None,
        'source': None,
        'description': None,
        'sequence': None
    }
    user = log_user(request)
    if raw_query:
        if not raw_query.startswith("NC_"):
            context['fasta'], context['description'], context['sequence'] = get_fasta(raw_query)
            print(context['description'])
        query, created = Query.objects.get_or_create(raw_query=context['raw_query'], fasta=context['fasta'], user=user)
        if not created:
            query.num_queries += 1
            query.save()
    return render(request, 'find/query.html', context)
