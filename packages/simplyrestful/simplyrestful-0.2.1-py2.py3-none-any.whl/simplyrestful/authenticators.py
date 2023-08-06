
class Authenticator(object):
    def authenticate(self):
        pass


class NullAuthenticator(Authenticator):
    def authenticate(self):
        return 1
