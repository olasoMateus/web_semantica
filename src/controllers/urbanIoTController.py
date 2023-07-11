from flask import Flask, request
from flask_restx import Api, Resource
from SPARQLWrapper import SPARQLWrapper, JSON

from src.server.instance import server
from src.models.urbanIotModel import urbanIoT

app = server.app
api = server.api

@api.route('/urbanIoT/especifiedQuery')
class UrbanIot(Resource):
    @api.doc(params={'Query': 'A query'})
    def get(self):
        sparql = SPARQLWrapper(
        "http://localhost:3030/urbanIoT/sparql"
        )
        sparql.setReturnFormat(JSON)

        print(1)

        query = request.args.get('Query', type = str)

        print(query)

        # gets the first 3 geological ages
        # from a Geological Timescale database,
        # via a SPARQL endpoint
        sparql.setQuery(query)

        try:
            ret = sparql.queryAndConvert()

            return ret

        except Exception as e:
            print(e)
            return "Erro"