# FastaFinder

FastaFinder is a tool for quickly finding the FASTA sequence given only an accession number.
Dedicated server to come!

## Installation
Clone the repository and use a python3 virtualenv to install python requirements.
```bash
>>> git clone https://github.com/liamhawkins/FastaFinder.git
>>> cd FastaFinder
>>> virtualenv venv -p $(which python3)
>>> source venv/bin/activate
>>> pip install -r requirements.txt
```

## Usage
Launch the Django web server
```bash
>>> python manage.py runserver
```
Then point your browser to the web server

`http://127.0.0.1:8000/`

You can directly query an accession by appending it to the url

`http://127.0.0.1:8000/P04797`

Which returns the Uniprot Human GAPDH Fasta sequence! Cool!

## Supported Accession IDs
Currently the following accessions are supported:

| Source | Example |
| --- | --- |
| Uniprot | P04797 |
| NCBI Refseq | NP_001243728.1 |
| MirBase ID | MI0000060 |
| MicroRNA name | hsa-let-7a-1 |