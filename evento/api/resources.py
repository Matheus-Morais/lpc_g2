from tastypie.resources import ModelResource
from tastypie import fields, utils
from evento.models import *
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
from tastypie.authentication import *
from django.contrib.auth.models import User

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['password', 'is_active']

class PessoaResource(ModelResource):
    usuario = fields.ToOneField(UserResource, 'usuario')
    class Meta:
        queryset = Pessoa.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()
        #authentication = ApiKeyAuthentication()
        filtering = {
            "descricao": ('exact', 'startswith')
        }

class EventoResource(ModelResource):
    def obj_create(self, bundle, **kwargs):
        userLogado = bundle.request.user
        if userLogado.is_superuser:
            evento = Evento()

            r = bundle.data['realizador'].split('/')
            evento.nome = bundle.data['nome']
            evento.sigla = bundle.data['sigla']
            evento.realizador = Pessoa.objects.get(pk = int(r[4]))

            evento.save()

            bundle.obj = evento
            return bundle
        else:
            raise Unauthorized("Você não tem autorização!")

    def obj_update(self, bundle, skip_errors=False, **kwargs):
        userLogado = bundle.request.user
        eventoGet = Evento.objects.get(pk=int(kwargs['pk']))
        if userLogado.is_superuser:
            r = bundle.data['realizador'].split('/')

            eventoGet.nome = bundle.data['nome']
            eventoGet.sigla = bundle.data['sigla']
            eventoGet.realizador = Pessoa.objects.get(pk=int(r[4]))
            eventoGet.dataEHoraDeInicio = bundle.data['dataEHoraDeInicio']

            eventoGet.save()

            bundle.obj = eventoGet
            return bundle
        else:
            raise Unauthorized("Você não tem autorização!")

    def obj_delete(self, bundle, **kwargs):
        userLogado = bundle.request.user
        event = Evento.objects.get(pk=int(kwargs['pk']))
        if userLogado.is_superuser:
            if Inscricoes.objects.filter(evento = event) or ArtigoCientifico.objects.filter(evento = event):
                raise Unauthorized("Evento tem inscritos ou artigos submetidos!")
            else:
                event.delete()
        else:
            raise Unauthorized("Você não é administrador!")

    def obj_get_list(self, bundle, **kwargs):
        userLogado = bundle.request.user
        if Autor.objects.filter(usuario=userLogado) or userLogado.is_superuser:
            return Evento.objects.all()
        else:
            raise Unauthorized("Você não tem autorização!")

    def obj_get(self, bundle, **kwargs):
        userLogado = bundle.request.user
        eventoGet = Evento.objects.get(pk=int(kwargs['pk']))
        if userLogado.is_superuser:
            return eventoGet
        else:
            raise Unauthorized("Você não tem autorização!")

    realizador = fields.ToOneField(PessoaResource, 'realizador')
    class Meta:
        queryset = Evento.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        #authorization = Authorization()
        authentication = ApiKeyAuthentication()
        filtering = {
            "descricao": ('exact', 'startswith')
        }

class EventoCientificoResource(ModelResource):
    def obj_create(self, bundle, **kwargs):
        userLogado = bundle.request.user
        if userLogado.is_superuser:
            evento = EventoCientifico()

            r = bundle.data['realizador'].split('/')
            evento.nome = bundle.data['nome']
            evento.realizador = Pessoa.objects.get(pk=int(r[4]))
            evento.issn = bundle.data['issn']

            evento.save()

            bundle.obj = evento
            return bundle
        else:
            raise Unauthorized("Você não tem autorização!")

    def obj_update(self, bundle, skip_errors=False, **kwargs):
        userLogado = bundle.request.user
        eventoGet = EventoCientifico.objects.get(pk=int(kwargs['pk']))
        if userLogado.is_superuser:
            r = bundle.data['realizador'].split('/')

            eventoGet.nome = bundle.data['nome']
            eventoGet.sigla = bundle.data['sigla']
            eventoGet.realizador = Pessoa.objects.get(pk=int(r[4]))
            eventoGet.dataEHoraDeInicio = bundle.data['dataEHoraDeInicio']
            eventoGet.issn = bundle.data['issn']

            eventoGet.save()

            bundle.obj = eventoGet
            return bundle
        else:
            raise Unauthorized("Você não tem autorização!")

    def obj_delete(self, bundle, **kwargs):
        userLogado = bundle.request.user
        event = EventoCientifico.objects.get(pk=int(kwargs['pk']))
        if userLogado.is_superuser:
            if Inscricoes.objects.filter(evento=event) or ArtigoCientifico.objects.filter(evento=event):
                raise Unauthorized("Evento tem inscritos ou artigos submetidos!")
            else:
                event.delete()
        else:
            raise Unauthorized("Você não é administrador!")

    def obj_get_list(self, bundle, **kwargs):
        userLogado = bundle.request.user
        # p = Pessoa.objects.filter(usuario = userLogado)
        if Autor.objects.filter(usuario=userLogado) or userLogado.is_superuser:
            return EventoCientifico.objects.all()
        else:
            raise Unauthorized("Você não tem autorização!")

    def obj_get(self, bundle, **kwargs):
        userLogado = bundle.request.user
        eventoGet = EventoCientifico.objects.get(pk=int(kwargs['pk']))
        if userLogado.is_superuser:
            return eventoGet
        else:
            raise Unauthorized("Você não tem autorização!")

    realizador = fields.ToOneField(PessoaResource, 'realizador')
    class Meta:
        queryset = EventoCientifico.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        # authorization = Authorization()
        authentication = ApiKeyAuthentication()
        filtering = {
            "descricao": ('exact', 'startswith')
        }

class ArtigoCientificoResource(ModelResource):
    def obj_create(self, bundle, **kwargs):
        userLogado = bundle.request.user

        if Autor.objects.filter(usuario = userLogado):
            artigo = ArtigoCientifico()
            artAutor = ArtigoAutor()

            e = bundle.data['EventoCientifico'].split('/')

            artigo.titulo = bundle.data['titulo']
            artigo.resumo = bundle.data['resumo']
            artigo.palavras_chave = bundle.data['palavras_chave']
            artigo.evento = EventoCientifico.objects.get(pk = int(e[4]))
            artigo.save()
            artAutor.artigoCientifico = ArtigoCientifico.objects.get(pk = artigo.pk)
            artAutor.autor = Autor.objects.get(usuario = userLogado)
            artAutor.save()
            bundle.obj = artigo
            return bundle
        else:
            raise Unauthorized("Você não é autor!")

    def obj_delete(self, bundle, **kwargs):
        userLogado = bundle.request.user
        aut = Autor.objects.filter(usuario = userLogado)
        art = ArtigoCientifico.objects.get(pk=int(kwargs['pk']))
        if ArtigoAutor.objects.filter(autor = aut, artigoCientifico = art):
            if AvaliacaoArtigo.objects.filter(artigo = art):
                raise Unauthorized("Artigo tem avaliação!")
            else:
                art.delete()
        else:
            raise Unauthorized("Você não tem autorização!")

    def obj_get_list(self, bundle, **kwargs):
        userLogado = bundle.request.user
        artigos = []
        aut = Autor.objects.filter(usuario = userLogado)
        aval = Avaliador.objects.filter(usuario=userLogado)
        if Autor.objects.filter(usuario = userLogado):
            autorArt = ArtigoAutor.objects.filter(autor = aut)
            for x in autorArt:
                a = ArtigoCientifico.objects.get(pk = int(x.artigoCientifico.pk))
                artigos.append(a)
            return artigos
        elif Avaliador.objects.filter(usuario = userLogado):
            avaliaEvento = AvaliadorEvento.objects.filter(avaliador=aval)
            for x in avaliaEvento:
                a = ArtigoCientifico.objects.get(evento = x.evento)
                artigos.append(a)
            return artigos
        else:
            raise Unauthorized("Você não tem autorização!")

    evento = fields.ToOneField(EventoResource, 'evento')
    class Meta:
        queryset = ArtigoCientifico.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        # authorization = Authorization()
        authentication = ApiKeyAuthentication()
        filtering = {
            "descricao": ('exact', 'startswith')
        }

class AvaliadorResource(ModelResource):
    usuario = fields.ToOneField(UserResource, 'usuario')
    class Meta:
        queryset = Avaliador.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()
        #authentication = ApiKeyAuthentication()
        filtering = {
            "descricao": ('exact', 'startswith')
        }

class CriterioAvaliacaoResource(ModelResource):
    class Meta:
        queryset = CriterioAvaliacao.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()
        #authentication = ApiKeyAuthentication()
        filtering = {
            "descricao": ('exact', 'startswith')
        }

class AvaliacaoArtigoResource(ModelResource):
    def obj_create(self, bundle, **kwargs):
        userLogado = bundle.request.user
        a = bundle.data['avaliador'].split('/')
        ar = bundle.data['artigo'].split('/')
        c = bundle.data['criterio'].split('/')
        if Avaliador.objects.filter(usuario = userLogado):
            avalia = AvaliacaoArtigo()

            avalia.avaliador = Avaliador.objects.get(pk = int(a[4]))
            avalia.artigo = ArtigoCientifico.objects.get(pk = int(ar[4]))
            avalia.criterio = CriterioAvaliacao.objects.get(pk = int(c[4]))
            avalia.nota = int(bundle.data['nota'])

            avalia.save()
            bundle.obj = avalia
            return bundle
        else:
            raise Unauthorized("Você não tem autorização!")

    def obj_delete(self, bundle, **kwargs):
        userLogado = bundle.request.user
        avaliacao = AvaliacaoArtigo.objects.get(pk = int(kwargs['pk']))
        a = avaliacao.avaliador
        if userLogado == a.usuario:
            avaliacao.delete()
        else:
            raise Unauthorized("Você não tem autorização!")

    avaliador = fields.ToOneField(AvaliadorResource, 'avaliador')
    artigo = fields.ToOneField(ArtigoCientificoResource, 'artigo')
    criterio = fields.ToOneField(CriterioAvaliacaoResource, 'criterio')
    class Meta:
        queryset = AvaliacaoArtigo.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authentication = ApiKeyAuthentication()
        filtering = {
            "descricao": ('exact', 'startswith')
        }