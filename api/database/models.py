import time

from mongoengine import *
import json


class Checkpoint(EmbeddedDocument):
    """
    A MongoEngine EmbeddedDocument containing:
        distance: MongoEngine float field, required, (checkpoint distance in kilometers),
		location: MongoEngine string field, optional, (checkpoint location name),
		open_time: MongoEngine datetime field, required, (checkpoint opening time),
		close_time: MongoEngine datetime field, required, (checkpoint closing time).
    """
    distance = FloatField(min_value=0.0, required=True)
    location = StringField()
    open_time = DateTimeField(required=True)
    close_time = DateTimeField(required=True)


class Brevet(Document):
    """
    A MongoEngine document containing:
		length: MongoEngine float field, required
		start_time: MongoEngine datetime field, required
		checkpoints: MongoEngine list field of Checkpoints, required
    """
    length = FloatField(required=True)
    start_time = DateTimeField(required=True)
    checkpoints = ListField(EmbeddedDocumentField(Checkpoint), required=True)

    @classmethod
    def from_request(cls, request):
        data = request.get_data(as_text=True)
        data = json.loads(data)

        # Sanity checking.
        if not any(d for d in data['distances'] if d):
            raise ValueError('Request had unspecified distances')

        # Create brevet.
        return Brevet(
            length=data['length'],
            start_time=data['start_time'],
            checkpoints=[
                Checkpoint(
                    distance=distance,
                    location=location,
                    open_time=open_time,
                    close_time=close_time,
                )
                for distance, location, open_time, close_time in zip(data['distances'], data['locations'], data['open_times'], data['close_times'])
                if distance and open_time and close_time
            ]
        )
