import bottle
import threading


class EkkoRemoteControl:
    """
    Minimalistic web api for interacting with the TS3ClientQuery. 
    
    Currently only implements ``whoami`` and ``sendtextmessage`` commands, but can be extended at will if required.

    Currently only used for debugging and testing purposes.
    """
    def __init__(self, ekkobot, web_port: int = 8080):
        self._ekko_app = ekkobot
        self._app = bottle.Bottle()
        self._routes()
        self.web_port = web_port

    def _routes(self):
        self._app.route('/ts3/whoami', callback=self.whoami)
        self._app.route('/ts3/sendtextmessage/<targetmode>/<target>/<message>', callback=self.message)

    def message(self, targetmode, target, message):
        self._ekko_app.create_connection().sendtextmessage(targetmode=targetmode, target=target, msg=message)
        return f'message "{message}" has been sent to targetmode={targetmode} w/ target={target}'

    def whoami(self):
        whoami = self._ekko_app.create_connection().whoami()
        return bottle.template('{{whoami}}', whoami=whoami)

    def main(self):
        threading.Thread(target=self._app.run, kwargs=dict(host='0.0.0.0', port=self.web_port)).start()
