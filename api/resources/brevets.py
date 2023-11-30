"""
Resource: Brevets
"""
from flask import Response, request
from flask_restful import Resource
from database.models import Brevet as MongoBrevet
import json


class Brevets(Resource):

    def get(self):
        """
        Displays latest brevet in database.
        """
        self.app.logger.debug('Brevets.get()')

        brevets = [
            brevet.to_json()
            for brevet in MongoBrevet.objects()
        ]
        self.app.logger.debug(f'brevets: {brevets}')

        return Response(
            json.dumps({'data': brevets}),
            status=200
        )

    def post(self):
        """
        Inserts a brevet object (defined in request) into the database.
        """
        self.app.logger.debug('Brevets.post()')

        # Create brevet.
        try:
            brevet = MongoBrevet.from_request(request)
            self.app.logger.debug(f'brevet: {brevet}')
            brevet.save()
        except Exception as e:
            self.app.logger.debug('Brevets.post failure')
            self.app.logger.debug(e)
            return {}, 400

        # Return result.
        self.app.logger.debug(f'Brevets.post success - id out: {brevet.id}')
        try:
            brevet_id = str(brevet.id)
        except Exception as e:
            self.app.logger.debug('Brevets.post id conversion fail')
            self.app.logger.debug(e)
            return {}, 400

        return Response(
            brevet_id,
            status=200
        )

    @property
    def app(self):
        from flask_api import app
        return app
