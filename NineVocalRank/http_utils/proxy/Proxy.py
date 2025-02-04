class Proxy:
    """
    代理类
    记录此代理的IP，协议类型
    """

    def __init__(self, ip: str = None, is_https: bool = False):
        self._ip = ip
        self._is_https = is_https

    @property
    def ip(self):
        return self._ip

    @property
    def is_https(self):
        return self._is_https

    def json(self):
        if self._ip is None:
            return dict()
        if self.is_https:
            return {"https": self._ip}
        else:
            return {"http": self._ip}
