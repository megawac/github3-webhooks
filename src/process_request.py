import json

from hashlib import sha1
import hmac

class AuthenticationError(Exception):
    pass

def process_request(content, secret=None, signature=None):
  """ Process the contents of a request (i.e. a post from GitHub's webhook service).
    This implementation is(/will be) web server agnostic.
  :param str content: The (string) body of the post from 
  :param str secret: (optional) A value used to compute the `X-Hub-Signature` header
  :param str signature: (optional) The value of the `X-Hub-Signature` header of the request
      used to verify the identity and intent of the request.
  """

  pass