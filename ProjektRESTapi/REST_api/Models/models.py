from tornado_swagger.components import components

@components.schemas.register
class PlayerModel(object):
    """
    ---
    type: object
    description: Player model representation
    properties:
        id:
            type: integer
            format: int64
        nick:
            type: string
        points_record:
            type: integer
            format: int64
            default: 0
        no_msg_sended:
            type: integer
            format: int64
            default: 0
        no_msg_received:
            type: integer
            format: int64
            default: 0
    """