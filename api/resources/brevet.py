"""
Resource: Brevet
"""
from flask import Response, request
from flask_restful import Resource
from database.models import Brevet as MongoBrevet


class Brevet(Resource):

    def get(self, brevet_id):
        """
        Return a brevet with the specified ID.
        """
        print(f'Brevet.get({brevet_id})')

        try:
            brevet = MongoBrevet.objects.get(id=brevet_id)
        except Exception as e:
            print('Brevet.get failure')
            print(e)
            return {}, 400

        # Sanity checking.
        if not brevet:
            print('Brevet.get failure -- no brevet')
            return {}, 400

        # Return our brevet.
        return Response(
            brevet.to_json(),
            mimetype="application/json",
            status=200
        )

    def delete(self, brevet_id):
        """
        Delete brevet with the specified ID.
        """
        print(f'Brevet.delete({brevet_id})')

        try:
            brevet = MongoBrevet.objects.get(id=brevet_id)
        except Exception as e:
            print('Brevet.delete failure 1')
            print(e)
            return {}, 400

        # Sanity checking.
        if not brevet:
            print('Brevet.delete failure -- no brevet')
            return {}, 400

        # Attempt deletion.
        try:
            brevet.delete()
        except Exception as e:
            print('Brevet.delete failure 2')
            print(e)
            return {}, 400

        # Deletion was successful.
        return {}, 200

    def put(self, brevet_id):
        """
        Update brevet with the specified ID, using object in request.
        """
        print(f'Brevet.put({brevet_id})')

        # Get existing brevet.
        try:
            existing_brevet = MongoBrevet.objects.get(id=brevet_id)
        except Exception as e:
            print('Brevet.put failure 1')
            print(e)
            return {}, 400

        # Get updated brevet model.
        try:
            updated_brevet = MongoBrevet.from_request(request)
        except Exception as e:
            print('Brevet.put failure 2')
            print(e)
            return {}, 400

        # Update existing brevet to updated one and save it.
        try:
            existing_brevet.length = updated_brevet.length
            existing_brevet.start_time = updated_brevet.start_time
            existing_brevet.checkpoints = updated_brevet.checkpoints
            existing_brevet.save()
        except Exception as e:
            print('Brevet.put failure 3')
            print(e)
            return {}, 400

        # Success
        return {}, 200
