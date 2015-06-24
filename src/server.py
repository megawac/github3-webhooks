from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.resource import Resource

import json, hmac
from hashlib import sha1

from blinker import signal

class WebhookServer(Resource):
  isLeaf = True

  def __init__(self, secret=None):
    """
    :param str secret: (optional) A value used to compute the `X-Hub-Signature` header
    """
    self.secret = secret

  def render_POST(self, request):
    """
    Process the contents of a request (i.e. a post from GitHub's webhook service)
    """
    content = request.content.read()

    # The value of the `X-Hub-Signature` header of the request
    # used to verify the identity and intent of the request.
    signature = request.getHeader("X-Hub-Signature")
    event = request.getHeader("X-GitHub-Event")

    if signature is None or event is None:
      request.setResponseCode(400)
      return "Request is missing required headers"

    # Validate the signature if provided, following these guidelines:
    # http://pubsubhubbub.googlecode.com/svn/trunk/pubsubhubbub-core-0.3.html#authednotify
    if self.secret is not None:
      hash = hmac.new(self.secret, content, sha1)
      if hash.digest().encode("hex") != signature[5:]:
        # This should return a 200 response regardless of failure to validate (by spec)
        request.setResponseCode(200)
        return "Could not identify the request's signature"

    data = json.loads(content)
    # Call listeners listening for the Webhook in a different thread
    reactor.callInThread(signal(event), data)
    return ""

  def start(self, port):
      factory = Site(self)
      reactor.listenTCP(port, factory)
      reactor.run()
