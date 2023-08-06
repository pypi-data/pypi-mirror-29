class ApiUrl(object):
    def __init__(self, protocol, port, domain, remainder, **kwargs):
        self.protocol = protocol
        self.port = port
        self.domain = domain
        self.remainder = remainder
        self.kwargs = kwargs

    def __getattr__(self, key):
        return self.kwargs[key]

    def as_dict(self):
        return_val = {
            'protocol': self.protocol,
            'domain': self.domain,
            'port': self.port,
            'remainder': self.remainder,
        }

        for key, value in self.kwargs.items():
            return_val[key] = value

        return return_val
