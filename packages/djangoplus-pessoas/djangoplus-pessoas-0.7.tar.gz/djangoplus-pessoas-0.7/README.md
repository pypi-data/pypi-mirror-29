Pessoas
=======

Pessoas is simple djangoplus application that contains classes for representing citizens and companies in Brazil.
It has three model classes:

- Pessoa
- PessoaJuridicaAbstrata
- PessoaFisicaAbstrata

### Dependecies

- djangoplus_enderecos

### Steps

Execute the following steps to use it:

1. Install it

    pip install djangoplus_pessoas djangoplus_enderecos


1. Add "pessoas" and "enderecos" to your INSTALLED_APPS settings

    INSTALLED_APPS = \[..., 'pessoas', 'enderecos']

2. Create the tables

    sync

3. Use the models

