from tornado_swagger.components import components

@components.schemas.register
class HistoriesSchema(object):
    """
    ---
    type: object
    description: Histories schema
    properties:
        date:
            type: string
        g_name:
            type: string
        players_tab:
            type: array
            items:
                type: object
                properties:
                    nick:
                        type: string
                    points:
                        type: integer
    """