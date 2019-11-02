from django.http import HttpResponse


def find_fasta(request, accession=None):
    if not accession:
        return HttpResponse('Invalid Query')
    else:
        return HttpResponse('{}'.format(accession))