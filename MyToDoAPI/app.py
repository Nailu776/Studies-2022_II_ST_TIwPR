from tornado.web import Application, RequestHandler, url
from tornado.ioloop import IOLoop
import tornado.options 
import json
from tornado_swagger.setup import setup_swagger
items = []


class TodoItems(RequestHandler):
  def get(self):
      """
        Description end-point
        ---
        tags:
        - Todos
        summary: Get items from todo List.
        description: 
        operationId: get_items_id
        requestBody: false
        responses:
            "200":
                description: Todo items getted.
        """
      self.write({'items': items})


class TodoItem(RequestHandler):
  def post(self, _):
      """
        Description end-point
        ---
        tags:
        - Todos
        summary: Add new item to todo List.
        description: 
        operationId: post_item_id        
        parameters:
          - name: id
            in: path
            description: ID of post to return
            required: true
            schema:
              type: integer
              format: int64
        requestBody:
          description: Created todo item
          required: false
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: integer
                    format: int64
                  name:
                    type:
                      - "string"
        responses:
            "200":
                description: Todo item created.
        """
      items.append(json.loads(self.request.body))
      self.write({'message': 'new item added'})

  def delete(self, id):      
      """
        Description end-point
        ---
        tags:
        - Todos
        summary: Delete todo by ID
        description: Returns deleted id
        operationId: deleteTaskById
        parameters:
          - name: id
            in: path
            description: ID of post to return
            required: true
            schema:
              type: integer
              format: int64
        responses:
            "200":
                description: Todo item deleted.
        """
      global items
      new_items = [item for item in items if item['id'] is not int(id)]
      items = new_items
      self.write({'message': 'Item with id %s was deleted' % id})




class Application(Application):
    _routes = [
        url("/items/", TodoItems, name= "TodoItems"),
        url(r"/api/item/([^/]+)?", TodoItem, name= "TodoItem"),
        ]
    def __init__(self):
        settings = {
            "debug": True,
            "autoreload": True
            }
        setup_swagger(
            self._routes, 
            swagger_url="/doc"
            )
        super(Application, self).__init__(self._routes, **settings)


if __name__ == "__main__":
    tornado.options.define("port", default="8080", help="Port to listen on")
    tornado.options.parse_command_line()
    app = Application()
    app.listen(port=8080)
    IOLoop.current().start()