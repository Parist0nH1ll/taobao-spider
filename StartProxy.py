from mitmproxy.tools.main import mitmweb

mitmweb(args=['-s', './HttpProxy.py', '-p', '9000', '--web-port', '9020'])