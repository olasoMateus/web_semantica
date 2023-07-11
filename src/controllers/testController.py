from flask import Flask, request
from flask_restx import Api, Resource
from SPARQLWrapper import SPARQLWrapper, JSON

from src.server.instance import server
from src.models.testModel import test

app = server.app
api = server.api

@api.route('/allThings')
class TestController(Resource):

    def get(self):
        sparql = SPARQLWrapper(
        "http://localhost:3030/urbanIoT/sparql"
        )
        sparql.setReturnFormat(JSON)

        query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT * WHERE {   ?sub ?pred ?obj . }
        """

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