import sys
sys.path.append("./gen-py")

import FutureService
from ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
import predictService
import newsRelateService

class ServiceHandler:
    def futureRelatedNews(self, future):
        tool = newsRelateService.newsService()
        result = tool.relateNews(future)
        return result
        # data = tool.relateNews(future)
        # result = list()
        # for i in data:
        #     print data[0], data[1], data[3]
        #     result.append(News(url=data[0], title=data[1], related=0.25, content=data[3]))
        # return result
        # l = list()
        # l.append(News(url=" s", title="ss", related=1.6, content="sdd "))
        # return l

    def predictPrice(self, future, type):
        print future + " predicted"
        tool = predictService.Predict()
        tool.fit(future)
        result = tool.getPridict(15)
        print result
        return result

class MyTBinaryProtocol(TBinaryProtocol.TBinaryProtocol):
	def __init__(self, trans, strictRead=False, strictWrite=True):
		TBinaryProtocol.TBinaryProtocol.__init__(self, trans, strictRead, strictWrite)

	def writeString(self, str):
		if type(str) is unicode:
			str = str.encode('utf-8')
		self.writeI32(len(str))
		self.trans.write(str)

class MyTBinaryProtocolFactory(TBinaryProtocol.TBinaryProtocolFactory):
	def __init__(self, strictRead=False, strictWrite=True):
		TBinaryProtocol.TBinaryProtocolFactory.__init__(self, strictRead, strictWrite)

	def getProtocol(self, trans):
		prot = MyTBinaryProtocol(trans, self.strictRead, self.strictWrite)
		return prot

handler = ServiceHandler()
processor = FutureService.Processor(handler)
transport = TSocket.TServerSocket("192.168.1.109", "8888")
tfactory = TTransport.TBufferedTransportFactory()
pfactory = MyTBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
print "server start"
server.serve()