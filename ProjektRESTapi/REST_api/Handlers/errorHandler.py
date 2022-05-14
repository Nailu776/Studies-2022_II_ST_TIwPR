from http import HTTPStatus
import http.client
from tornado.web            import RequestHandler, ErrorHandler
import hashlib
from asyncio.windows_events import NULL
from typing import   Optional

# Err Desc  
errData = {}
errData['Cause'] = 'Something is wrong.' 

class BaseHandler(RequestHandler):
  # Override etag functions
  # Check if etag match
  def check_if_match(self) -> bool:
    # Set new etag (hash of the conent written so far)
    self.set_my_etag_header()
    # Vanish get player response
    self._write_buffer=[]
    # Check if etag in request exists
    req_etag = self.request.headers.get("If-Match", "")
    if req_etag:
      # NOTE check_etag_header checks the ``Etag`` header against 
      # requests's ``If-None-Match``
      self.request.headers['If-None-Match'] = req_etag
      # Check etag: if equals then entity is not modified
      if not self.check_etag_header():
        # Etag changed so entitiy is modified
        errData['Cause'] = 'Entity changed.'
        self.set_status(HTTPStatus.PRECONDITION_FAILED)
        return False
      else:
        # Go on you got up-to-date entity
        return True
    else:
      errData['Cause'] = 'ETag is missing.'
      self.set_status(HTTPStatus.PRECONDITION_REQUIRED)
      return False
  # Check if entity is modified
  def check_modified_resp(self):
    # Set new etag (hash of the conent written so far)
    self.set_my_etag_header()
    # Check etag: if equals then response is not modified
    if self.check_etag_header():
      # Vanish response (for 304)
      self._write_buffer = []
      # Error Code 304 Not Modified 
      self.set_status(HTTPStatus.NOT_MODIFIED)
      return
    else:
      # Etag changed so return with response body
      return
  # Compute etag on finish (tornado feature)   
  def compute_etag(self):
    """Computes the etag header to be used for this request.

    By default uses a hash of the content written so far.

    May be overridden to provide custom etag implementations,
    or may return None to disable tornado's default etag support.
    """
    # Overridde it
    return NULL
  # Compute actual etag   
  def compute_my_etag(self) -> Optional[str]:
      """Computes the etag header to be used for this request.
      By default uses a hash of the content written so far.
      """
      hasher = hashlib.sha1()
      for part in self._write_buffer:
          hasher.update(part)
      return '"%s"' % hasher.hexdigest()
  # Set etag for custom etag implementation  
  def set_my_etag_header(self) -> None:
      """Sets the response's Etag header using ``self.compute_etag()``.

      Note: no header will be set if ``compute_etag()`` returns ``None``.

      This method is called automatically when the request is finished.
      """
      # Overridden function to provide custom etag implementation
      etag = self.compute_my_etag()
      if etag is not None:
          self.set_header("Etag", etag)
  # Write error  
  def write_error(self, status, **kwargs):
    self.write("HTTP error code: {} {}\n".format(str(status),
                http.client.responses[status]))  
    self.write("Cause: " + errData['Cause'])
  # Add link header with prev and/or next page
  def add_link_header(self, endpoint, counter_query, cursor, offset, limit, page):
    # Number of entities in table
    cursor.execute(counter_query)
    no_entities = cursor.fetchone()
    # Add link header next or/and prev page
    if ((no_entities[0] - offset - limit) > 0) and (offset > 0):
      # Number of entities - omitted offset - getted limit > 0 --> got next page
      # and
      # offset > 0 --> got prev page
      # print("case 1 " + str(page) + " " + str(limit) + " " + str(no_entities[0]) )
      nextpage = "<http://localhost:8000/"+ endpoint + "/?limit=" + str(limit) + "&page=" + str(page + 1) + ">; rel=\"next\"; "
      prevpage = "<http://localhost:8000/"+ endpoint + "/?limit=" + str(limit) + "&page=" + str(page - 1) + ">; rel=\"prev\"; "
      self.add_header('Link', nextpage + prevpage)
    elif (offset > 0):
      # NOTE if you get e.g. page 10 of 2 pages you will get nothing + link to page 9 that will also give nothing.
      # offset > 0 --> got prev page ==> if so then ((no_entities[0] - offset - limit) <= 0) --> no next page
      # print("case 2 " + str(page) + " " + str(limit) + " " + str(no_entities[0]) )
      prevpage = "<http://localhost:8000/"+ endpoint + "/?limit=" + str(limit) + "&page=" + str(int(page - 1)) + ">; rel=\"prev\"; "
      self.add_header('Link', prevpage)
    elif ((no_entities[0] - offset - limit) > 0):
      # Number of entities - omitted offset - getted limit > 0 --> got next page
      # ==> if so then offset == 0 --> no prev page
      # print("case 3 " + str(page) + " " + str(limit) + " " + str(no_entities[0]) )
      nextpage = "<http://localhost:8000/"+ endpoint + "/?limit=" + str(limit) + "&page=" + str(page + 1) + ">; rel=\"next\"; "
      self.add_header('Link', nextpage)
    else:
      # print("case 4 " + "Nothing more to get.")
      # Interesting
      # offset == 0
      # and
      # ((no_entities[0] - offset - limit) <= 0)
      # so nothing to get and also nothing More to get
      pass

class ErrorHandler(ErrorHandler, BaseHandler):
    pass
