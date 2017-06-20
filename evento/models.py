from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Evento(models.Model):
    nome = models.CharField('nome', max_length=200)
    sigla = models.CharField('sigla', max_length=20)
    dataEHoraDeInicio = models.DateTimeField('dataEHoraDeInicio', default=timezone.now)
    realizador = models.ForeignKey('Pessoa')

    def save(self, *args, **kwargs):
        self.nome = self.nome.upper()

        super(Evento, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.nome)


class EventoCientifico(Evento):
    issn = models.CharField('issn', max_length=200)

    def __str__(self):
        return '{}'.format(self.issn)


class Pessoa(models.Model):
    nome = models.CharField('nome', max_length=200)
    email = models.CharField('email', max_length=200)
    usuario = models.ForeignKey(User)

    def __str__(self):
        return '{}'.format(self.nome)


class PessoaFisica(Pessoa):
    cpf = models.CharField('cpf', max_length=20)

    def __str__(self):
        return '{}'.format(self.cpf)


class PessoaJuridica(Pessoa):
    cnpj = models.CharField('cnpj', max_length=100)
    razaoSocial = models.CharField('razaoSocial', max_length=200)

    def __str__(self):
        return '{}'.format(self.cnpj)


class Autor(Pessoa):
    curriculo = models.CharField('curriculo', max_length=200)

    def __str__(self):
        return '{}'.format(self.nome)


class ArtigoCientifico(models.Model):
    titulo = models.CharField('titulo', max_length=200)
    resumo = models.CharField('resumo', max_length=500)
    palavras_chave = models.CharField('palavras_chave', max_length=200)
    evento = models.ForeignKey('EventoCientifico')

    def __str__(self):
        return '{}'.format(self.titulo)


class Inscricoes(models.Model):
    pessoa = models.ForeignKey('PessoaFisica')
    evento = models.ForeignKey('Evento')
    dataEHoraDaInscricao = models.DateTimeField('dataEHoraDaInscricao', default=timezone.now)
    tipoInscricao = models.ForeignKey('TipoInscricao')

    def __str__(self):
        return '{}'.format(self.pessoa)


class TipoInscricao(models.Model):
    descricao = models.CharField('descricao', max_length=200)

    def __str__(self):
        return '{}'.format(self.descricao)


class ArtigoAutor(models.Model):
    artigoCientifico = models.ForeignKey('ArtigoCientifico')
    autor = models.ForeignKey('Autor')

    def __str__(self):
        return '{}'.format(self.artigoCientifico)


class CriterioAvaliacao(models.Model):
    nome = models.CharField('Nome', max_length=200)


class Avaliador(Pessoa):
    curriculo = models.CharField('curriculo', max_length=200)

    def __str__(self):
        return '{}'.format(self.curriculo)

class AvaliadorEvento(models.Model):
    avaliador = models.ForeignKey('Avaliador')
    evento = models.ForeignKey('EventoCientifico')

class AvaliacaoArtigo(models.Model):
    avaliador = models.ForeignKey('Avaliador')
    artigo = models.ForeignKey('ArtigoCientifico')
    criterio = models.ForeignKey('CriterioAvaliacao')
    nota = models.IntegerField(null=True, blank=True)
    # C1Tecnica = models.CharField('C1Tecnica', max_length=200)
    # C2Inovacao = models.CharField('C2Inovacao', max_length=200)
    # C3Resulados = models.CharField('C3Resulados', max_length=200)
    # C4Metodologia = models.CharField('C4Metodologia', max_length=200)
    # C4Tematica = models.CharField('C4Tematica', max_length=200)
