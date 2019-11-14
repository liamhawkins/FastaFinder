from django.shortcuts import render
from ipware import get_client_ip

from find.models import User, Query, FastaSource
from find.sources import Uniprot, SequenceNotFoundError, NCBI, Mirbase, MicroRNA

sources = [Uniprot, Mirbase, MicroRNA, NCBI]


class NoMatchingSourceError(Exception):
    pass


def log_user(request):
    ip, is_routable = get_client_ip(request)
    user, created = User.objects.get_or_create(ip=ip)
    if not created:
        user.num_queries += 1
        user.save()
    return user


def is_genome(raw_query):
    return raw_query.startswith("NC_")


def get_fasta(query):
    try:
        fasta_source = FastaSource.objects.get(accession=query)
    except FastaSource.DoesNotExist:
        fasta_source = None

    for source in sources:
        if source.is_valid(query):
            return source.get(accession=query, fasta_source=fasta_source)
    raise NoMatchingSourceError("No source matches query: {}".format(query))

def query(request, raw_query=None):
    context = {
        'user': log_user(request),
        'raw_query': raw_query,
        'is_genome': None,
        'fasta_source': None,
        'source': None,
        'description': None,
        'sequence': None
    }

    if not raw_query:
        context['raw_query'] = None
    elif is_genome(raw_query):
        context['is_genome'] = True
    else:
        try:
            fasta = get_fasta(raw_query)
            context.update(fasta.to_dict())
        except (SequenceNotFoundError, NoMatchingSourceError) as e:
            print(str(e))
        Query.objects.create(raw_query=context['raw_query'], fasta_source=context['fasta_source'], user=context['user'])
    return render(request, 'find/query.html', context)
