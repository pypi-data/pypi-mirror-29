import socket
import json
import time

class ConnectionError(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)


class Logger():
    def __init__(self, host='127.0.0.1', port=8125, proto='print', tags=[], log_level='INFO'):
        self.host = host
        self.port = port
        self.tags = tags
        self.levels = {'ERROR':5, 'WARN':4, 'INFO':3, 'TRACE':2, 'DEBUG':1}
        self.log_level = log_level
        try:
            if proto == 'udp':
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.sock.connect((host,port))
            elif proto == 'tcp':
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((host,port))
            else:
                self.sock = None
        except Exception as e:
            raise ConnectionError('error connecting to remote agent')

    def set_tags(self, tags):
        self.tags = tags

    def debug(self,*args,**kwargs):
        level = 'DEBUG'
        if not self.levels[level] >= self.levels[self.log_level]:
            return
        return self._log(level=level,*args,**kwargs)

    def trace(self,*args,**kwargs):
        level = 'TRACE'
        if not self.levels[level] >= self.levels[self.log_level]:
            return
        return self._log(level=level,*args,**kwargs)


    def info(self,*args,**kwargs):
        level = 'INFO'
        if not self.levels[level] >= self.levels[self.log_level]:
            return
        return self._log(level=level,*args,**kwargs)


    def warn(self,*args,**kwargs):
        level = 'WARN'
        if not self.levels[level] >= self.levels[self.log_level]:
            return
        return self._log(level=level,*args,**kwargs)


    def error(self,*args,**kwargs):
        level = 'ERROR'
        if not self.levels[level] >= self.levels[self.log_level]:
            return
        return self._log(level=level,*args,**kwargs)


    def _log(self, msg, tags=[], level='INFO'):
        formatted_msg = {'@message': msg, '@tags': self.tags + tags, '@timestamp': time.time(), '@level': level}
        if self.sock:
            self.sock.send(json.dumps(formatted_msg).encode())
        else:
            print(json.dumps(formatted_msg))
        return


if __name__ == '__main__':
    """
    Example Implementation of the logger
    """
    print_log = Logger() # Creating Logger to print json
    print_log.debug('printing log...')

    tcp_log = Logger(host='1.2.3.4', port=8125, proto='tcp') # Creating Logger to send logs via TCP
    tcp_log.debug('sending log via TCP...')

    udp_log = Logger(host='server.example.com', port=8125, proto='udp') # Creating Logger to send logs via UDP
    udp_log.debug('sending log via UDP...')
