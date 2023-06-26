from socket import *
from select import *
class Http_server():
    # 成员变量
    def __init__(self, host, port=80, html=None):
        self.host = host
        self.port = port
        self.html = html
        self.ADDR = (host, port)
        self.soke = self.__sokes()
        self.rlist = []

    # 返回soke
    def __sokes(self):
        soke = socket()
        soke.bind(self.ADDR)
        soke.setblocking(False)
        return soke

    # 启动方法
    def mains(self):
        self.soke.listen(5)
        self.rlist.append(self.soke)
        while True:
            rs, ws, xs = select(self.rlist, [], [])
            for i in rs:
                if i is self.soke:
                    self.lianjie(i)
                else:
                    try:
                        self.jieshou(i)
                    except Exception as e:
                        print(e)
                    finally:
                        self.rlist.remove(i)
                        i.close()

    # 处理浏览器连接
    def lianjie(self,i):
        fd, addr = i.accept()
        # print(addr, '已链接')
        fd.setblocking(False)
        self.rlist.append(fd)

    # 处理接收消息
    def jieshou(self, fd):
        data = fd.recv(1024).decode()
        if not data:
            raise Exception
        msg = data.split(' ')[1]
        print('用户请求：', msg)
        self.__send_response(fd, msg)

    def __send_response(self, fd, msg):
        response = """HTTP/1.1 200 OK
Content-Type:text/html

""".encode()
        if msg == '/':
            file = self.html + "/index.html"
        else:
            file = self.html + msg
        try:
            f = open(file, 'rb')
        except:

            with open(self.html + '/404.html', 'rb') as f:
                data = f.read()
        else:
            with open(file, 'rb') as f:
                data = f.read()
        finally:
            htmls = response + data
            fd.send(htmls)


if __name__ == '__main__':
    start = Http_server(host='0.0.0.0', port=8889, html='/home/tarena/month02/day17/static')
    start.mains()
