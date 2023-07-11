from flask_restx import fields

from src.server.instance import server

urbanIoT = server.api.model('urbanIoT', {
    'Query': fields.String(required = True, description = 'A query desejada.')
})