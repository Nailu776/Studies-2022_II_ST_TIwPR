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
@components.schemas.register
class PlayerPatchSchema(object):
    """
    ---
    type: object
    description: Player patch schema
    properties:
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
@components.schemas.register
class PlayerUpdateSchema(object):
    """
    ---
    type: object
    description: Player model representation
    properties:
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

@components.schemas.register
class PlayerPostSchema(object):
    """
    ---
    type: object
    description: Player post schema
    properties:
        nick:
            type: string
    """
# @components.schemas.register
# class ArrayOfPlayers(object):
#     """
#     ---
#     definitions:
#         ArrayOfPlayers:
#             type: array
#             items:
#                 type: object
#                 properties:
#                     id:
#                         type: integer
#                         format: int64
#                     nick:
#                         type: string
#                     points_record:
#                         type: integer
#                         format: int64
#                         default: 0
#                     no_msg_sended:
#                         type: integer
#                         format: int64
#                         default: 0
#                     no_msg_received:
#                         type: integer
#                         format: int64
#                         default: 0
#             example:
#                 - id: 10
#                   nick: TypicalNickName
#                   points_record: 996
#                   no_msg_sended: 125
#                   no_msg_received: 200
#                 - id: 11
#                   nick: TypicalNickName2
#                   points_record: 995
#                   no_msg_sended: 124
#                   no_msg_received: 201
#     """