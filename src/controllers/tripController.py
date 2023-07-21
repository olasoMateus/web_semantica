from flask import Flask, request
from flask_restx import Api, Resource
from SPARQLWrapper import SPARQLWrapper, JSON

from src.server.instance import server
from src.models.testModel import test

app = server.app
api = server.api

@api.route('/tipByTime')
class tripByTime(Resource):
    @api.doc(params={'Minutos': 'Minutos minimos da viagem',
                     'Limite': 'O limite de resposta da query'}, responses={
        200: 'Success',
        400: 'Validation Error'},
        description='Retorna a URI da viagem, seu endereço de começo, de fim, o tipo de veículo e a duração para viagem com minutos maior ou igual ao informado.')
    def get(self):
        sparql = SPARQLWrapper(
        "http://18.230.197.243:3030/urbanIoT/query"
        )
        sparql.setReturnFormat(JSON)

        minutes = request.args.get('Minutos', type = str)
        limit = request.args.get('Limite', type = str)


        query = """PREFIX uiots: <http://www.w3id.org/urban-iot/sharing#>
                PREFIX sch: <http://schema.org/>

                SELECT ?sub ?startAddress ?endingAddress ?typeVehicle ?duration WHERE {
                    ?sub a uiots:SharingMobilityTrip .
                    ?sub uiots:tripDuration ?duration .
                    ?sub uiots:hasStartingStation ?start . 
                    ?start sch:address ?startAddress .
                    ?sub uiots:hasEndingStation ?ending . 
                    ?start sch:address ?endingAddress .
                    ?sub uiots:hasPropulsionKind ?typeVehicle
                    FILTER (?duration >= """ + minutes + """)
                }"""
        
        if(limit):
            query = query + " LIMIT " + limit


        sparql.setQuery(query)

        try:
            ret = sparql.queryAndConvert()

            return ret, 200

        except Exception as e:
            print(e)
            return "Erro", 400
        

@api.route('/tipByTypeOfVehicle')
class tripByTime(Resource):
    @api.doc(params={'Tipo': 'Tipo do veiculo da viagem (standard ou eletric)',
                     'Limite': 'O limite de resposta da query'}, responses={
        200: 'Success',
        400: 'Validation Error'},
        description='Retorna a URI da viagem, seu endereço de começo, de fim, o tipo de veículo e a duração para viagem com o tipo de veiculo informado')
    def get(self):
        sparql = SPARQLWrapper(
        "http://18.230.197.243:3030/urbanIoT/query"
        )
        sparql.setReturnFormat(JSON)

        type = request.args.get('Tipo', type = str)
        limit = request.args.get('Limite', type = str)


        query = """PREFIX uiots: <http://www.w3id.org/urban-iot/sharing#>
                PREFIX sch: <http://schema.org/>

                SELECT ?sub ?startAddress ?endingAddress ?typeVehicle ?duration WHERE {
                    ?sub a uiots:SharingMobilityTrip .
                    ?sub uiots:tripDuration ?duration .
                    ?sub uiots:hasStartingStation ?start . 
                    ?start sch:address ?startAddress .
                    ?sub uiots:hasEndingStation ?ending . 
                    ?start sch:address ?endingAddress .
                    ?sub uiots:hasPropulsionKind ?typeVehicle
                    FILTER REGEX(str(?typeVehicle), \"""" + type + """\", "i")
                }"""
        
        if(limit):
            query = query + " LIMIT " + limit


        sparql.setQuery(query)

        try:
            ret = sparql.queryAndConvert()

            return ret, 200

        except Exception as e:
            print(e)
            return "Erro", 400