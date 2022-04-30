from tornado_swagger.components import components

@components.schemas.register
class PlayerMergesSchema(object):
    """
    ---
    type: object
    description: Player Merges Schema
    properties:
        date:
            type: string
        nick_first:
            type: string
        nick_secound:
            type: string
        nick_finall:
            type: string
    """