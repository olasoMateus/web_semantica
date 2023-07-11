from flask_restx import fields

from src.server.instance import server

test = server.api.model('test', {
    'Query': fields.String(required = True, description = 'A query desejada.', enum = ["A", "B"])
})