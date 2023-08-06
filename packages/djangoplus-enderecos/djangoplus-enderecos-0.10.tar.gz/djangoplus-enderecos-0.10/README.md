Endereços
=======

Enderecos is a simple djangoplus app that contains all the regions, states, cities and neighborhoods of Brazil.

It has three model classes:

- Regiao
- Estado
- Municipio
- Endereco

### Dependecies

None

### Steps

Execute the following steps to use it:

1. Install it

    pip install djangoplus_enderecos


1. Add "enderecos" to your INSTALLED_APPS settings

    INSTALLED_APPS = \[..., 'enderecos']

2. Create the tables

    sync

3. Use the models

4. Load all cities (optional)

    python manage.py carregar_cidades

