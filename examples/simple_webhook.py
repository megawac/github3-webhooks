from src.server import WebhookServer
from blinker import signal

pr_signal = signal('pull_request')
issues_signal = signal('issues')
push_signal = signal('push')

class MyLibrary():
  def __init__():
    pass

  @pr_signal.connect
  def on_pull_request(self, data):
    print 'New pull request #%d' % data.get('number')

  @issues_signal.connect
  def on_issue(self, data):
    print 'New issue #%d' % data.get('number')

  @push_signal.connect
  def on_commit(self, data):
    print 'New commit'

server = WebhookServer()
server.start(9000)