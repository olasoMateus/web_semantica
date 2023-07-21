from flask import Flask, request
from flask_restx import Api, Resource
from SPARQLWrapper import SPARQLWrapper, JSON

from src.server.instance import server
from src.models.urbanIotModel import urbanIoT

app = server.app
api = server.api

@api.route('/especifiedQuery')
class UrbanIot(Resource):
    @api.doc(params={'Query': 'A query'}, responses={
        200: 'Success',
        400: 'Validation Error'},
        description='Permite que você realize qualquer query SPARQL na database.')
    def get(self):
        sparql = SPARQLWrapper(
        "http://18.231.162.156:3030/urbanIoT/query"
        )
        sparql.setReturnFormat(JSON)


        query = request.args.get('Query', type = str)
        
        sparql.setQuery(query)

        try:
            ret = sparql.queryAndConvert()

            return ret, 200

        except Exception as e:
            print(e)
            return "Erro", 400
        
@api.route('/allThings')
class AllThings(Resource):
    @api.doc(params={'Limite': 'Limite de itens retornados'}, responses={
        200: 'Success',
        400: 'Validation Error'},
        description='Retorna todos os itens, dado o limite informado.')
    def get(self):
        sparql = SPARQLWrapper(
        "http://18.231.162.156:3030/urbanIoT/query"
        )
        sparql.setReturnFormat(JSON)

        limit = request.args.get('Limite', type = int)

        query = """
        SELECT * WHERE {   ?sub ?pred ?obj . } LIMIT 
        """ + str(limit)

        sparql.setQuery(query)

        try:
            ret = sparql.queryAndConvert()

            return ret, 200

        except Exception as e:
            print(e)
            return "Erro", 400
        
@api.route('/activeStations')
class ActiveStations(Resource):
    @api.doc(params={'Limite': 'Limite de itens retornados'}, responses={
        200: 'Success',
        400: 'Validation Error'},
        description='Retorna a URI, o nome, o número de bicicletas, a latitude, a longitude e o endereço de todas as estações de compartilhamento de bicicleta ativas.')
    def get(self):
        sparql = SPARQLWrapper(
        "http://18.231.162.156:3030/urbanIoT/query"
        )
        sparql.setReturnFormat(JSON)

        query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX uiots: <http://www.w3id.org/urban-iot/sharing#>
        PREFIX name: <http://xmlns.com/foaf/0.1/name/>
        PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
        PREFIX sch: <http://schema.org/>

        SELECT ?sub ?name ?lat ?long ?address ?bikes WHERE {
            ?sub a uiots:PhysicalSharingStation .
            ?sub uiots:isStationActive ?state .
            ?sub uiots:AvailableVehicles ?bikes .
            ?sub name: ?name .
            ?sub geo:lat ?lat .
            ?sub geo:long ?long .
            ?sub sch:address ?address .
            FILTER (?state = true)
        }
        """

        sparql.setQuery(query)

        try:
            ret = sparql.queryAndConvert()

            return ret, 200

        except Exception as e:
            print(e)
            return "Erro", 400
        
@api.route('/numberOfBicycles')
class NumberOfBicycles(Resource):
    @api.doc(params={'Bicicletas': 'Número de bicicletas na estação'}, responses={
        200: 'Success',
        400: 'Validation Error'},
        description='Retorna a URI, o nome, o número de bicicletas, a latitude, a longitude e o endereço das estações que tem o número de bicicletas informadas, ou mais.')
    def get(self):
        sparql = SPARQLWrapper(
        "http://18.231.162.156:3030/urbanIoT/query"
        )
        sparql.setReturnFormat(JSON)

        bikes = request.args.get('Bicicletas', type = int)

        query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX uiots: <http://www.w3id.org/urban-iot/sharing#>
        PREFIX name: <http://xmlns.com/foaf/0.1/name/>
        PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
        PREFIX sch: <http://schema.org/>

        SELECT ?sub ?name ?lat ?long ?address ?bikes WHERE {
            ?sub a uiots:PhysicalSharingStation .
            ?sub uiots:AvailableVehicles ?bikes .
            ?sub name: ?name .
            ?sub geo:lat ?lat .
            ?sub geo:long ?long .
            ?sub sch:address ?address .
            FILTER (?bikes >= """ + str(bikes) + """)
        }
        """

        sparql.setQuery(query)

        try:
            ret = sparql.queryAndConvert()

            return ret, 200

        except Exception as e:
            print(e)
            return "Erro", 400
        
@api.route('/stationByAddress')
class NumberOfBicycles(Resource):
    @api.doc(params={'Endereco': 'Endereço da estação desejada'}, responses={
        200: 'Success',
        400: 'Validation Error'},
        description='Retorna a URI, o nome, o número de bicicletas, a latitude, a longitude e o endereço das estações que contém o endereço formado.')
    def get(self):
        sparql = SPARQLWrapper(
        "http://18.231.162.156:3030/urbanIoT/query"
        )
        sparql.setReturnFormat(JSON)

        address = request.args.get('Endereco', type = str)

        query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX uiots: <http://www.w3id.org/urban-iot/sharing#>
        PREFIX name: <http://xmlns.com/foaf/0.1/name/>
        PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
        PREFIX sch: <http://schema.org/>

        SELECT ?sub ?name ?lat ?long ?address ?bikes WHERE {
            ?sub a uiots:PhysicalSharingStation .
            ?sub uiots:AvailableVehicles ?bikes .
            ?sub name: ?name .
            ?sub geo:lat ?lat .
            ?sub geo:long ?long .
            ?sub sch:address ?address .
            FILTER REGEX(str(?address), \"""" + address + """\", "i")
        }
        """

        sparql.setQuery(query)

        try:
            ret = sparql.queryAndConvert()

            return ret, 200

        except Exception as e:
            print(e)
            return "Erro", 400