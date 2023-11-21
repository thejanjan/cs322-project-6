"""
Resource: Brevets
"""
from flask import Response, request
from flask_restful import Resource
from database.models import Brevet as MongoBrevet


class Brevets(Resource):

    def get(self):
        """
        Displays all brevets stored in the database.
        """
        print('Brevets.get()')

        return Response(
            {'brevets': [
                brevet.to_json()
                for brevet in MongoBrevet.objects()
            ]},
            mimetype="application/json",
            status=200
        )

    def post(self):
        """
        Inserts a brevet object (defined in request) into the database.
        """
        print('Brevets.post()')

        # Create brevet.
        try:
            brevet = MongoBrevet.from_request(request).save()
        except Exception as e:
            print('Brevets.post failure')
            print(e)
            return {}, 400

        # Return result.
        return {'brevet_id': brevet.id}
