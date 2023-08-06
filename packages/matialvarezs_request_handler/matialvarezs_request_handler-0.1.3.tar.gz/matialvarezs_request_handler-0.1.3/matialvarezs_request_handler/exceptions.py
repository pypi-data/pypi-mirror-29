

class Base(Exception):
    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)




class MethodNotSupported(Base):
    def __init__(self):
        super(MethodNotSupported, self).__init__("Method not supported")

class BadRequest(Base):
    def __init__(self):
        super(BadRequest, self).__init__("Bad request")

class Timeout(Base):
    def __init__(self):
        super(Timeout, self).__init__("Timeout")

class ConnectionError(Base):
    def __init__(self):
        super(ConnectionError, self).__init__("Connection error")


class MaxTriesReached(Base):
    def __init__(self):
        super(MaxTriesReached, self).__init__("Max tries reached")

    

