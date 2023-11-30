"""
Resource: Brevet
"""
from flask import Response, request
from flask_restful import Resource
from database.models import Brevet as MongoBrevet


class Brevet(Resource):

    def get(self, bid):
        """
        Return a brevet with the specified ID.
        """
        self.app.logger.debug(f'Brevet.get({bid})')

        try:
            brevet = MongoBrevet.objects.get(id=bid)
        except Exception as e:
            self.app.logger.debug('Brevet.get failure')
            self.app.logger.debug(e)
            return Response({}, mimetype="application/json", status=400)

        # Sanity checking.
        if not brevet:
            self.app.logger.debug('Brevet.get failure -- no brevet')
            return Response({}, mimetype="application/json", status=400)

        # Return our brevet.
        return Response(
            brevet.to_json(),
            status=200
        )

    def delete(self, bid):
        """
        Delete brevet with the specified ID.
        """
        self.app.logger.debug(f'Brevet.delete({bid})')

        try:
            brevet = MongoBrevet.objects.get(id=bid)
        except Exception as e:
            self.app.logger.debug('Brevet.delete failure 1')
            self.app.logger.debug(e)
            return Response({}, mimetype="application/json", status=400)

        # Sanity checking.
        if not brevet:
            self.app.logger.debug('Brevet.delete failure -- no brevet')
            return Response({}, mimetype="application/json", status=400)

        # Attempt deletion.
        try:
            brevet.delete()
        except Exception as e:
            self.app.logger.debug('Brevet.delete failure 2')
            self.app.logger.debug(e)
            return Response({}, mimetype="application/json", status=400)

        # Deletion was successful.
        return Response({}, mimetype="application/json", status=200)

    def put(self, bid):
        """
        Update brevet with the specified ID, using object in request.
        """
        self.app.logger.debug(f'Brevet.put({bid})')

        # Get existing brevet.
        try:
            existing_brevet = MongoBrevet.objects.get(id=bid)
        except Exception as e:
            self.app.logger.debug('Brevet.put failure 1')
            self.app.logger.debug(e)
            return Response({}, mimetype="application/json", status=400)

        # Get updated brevet model.
        try:
            updated_brevet = MongoBrevet.from_request(request)
        except Exception as e:
            self.app.logger.debug('Brevet.put failure 2')
            self.app.logger.debug(e)
            return Response({}, mimetype="application/json", status=400)

        # Update existing brevet to updated one and save it.
        try:
            existing_brevet.length = updated_brevet.length
            existing_brevet.start_time = updated_brevet.start_time
            existing_brevet.checkpoints = updated_brevet.checkpoints
            existing_brevet.save()
        except Exception as e:
            self.app.logger.debug('Brevet.put failure 3')
            self.app.logger.debug(e)
            return Response({}, mimetype="application/json", status=400)

        # Success
        return Response({}, mimetype="application/json", status=200)

    @property
    def app(self):
        from flask_api import app
        return app
