from tornado_swagger.components import components

@components.schemas.register
class MessagePostSchema(object):
    """
    ---
    type: object
    description: Message schema
    properties:
        sender_nick:
            type: string
        receiver_nick:
            type: string
        text_message:
            type: string
    """

@components.schemas.register
class MessageSchema(object):
    """
    ---
    type: object
    description: Message schema
    properties:
        id:
            type: integer
            format: int64
        sender_nick:
            type: string
        receiver_nick:
            type: string
        text_message:
            type: string
    """