import asyncio

class Broker:

    clients={}
    
    async def run(self):
        broker = await asyncio.start_server(self.gestisci_client,"127.0.0.1",8888)
        async with broker:
            await broker.serve_forever()

    async def pub(self,topic,msg):
        try:
            for writer in self.__class__.clients[topic][:]:
                writer.write(f"{msg}\n".encode())
                await writer.drain()
        except KeyError:
            pass


    async def gestisci_client(self,reader,writer):
        ip,pn = writer.get_extra_info("peername")
        print(f"Connesso: {ip}:{pn}")
        dati = await reader.readline()
        if not dati:
            print(f"Disconnesso: {ip}:{pn}")
            writer.close()
            await writer.wait_closed()
            return
        datas=dati.decode().rstrip().split(":")
        if datas[1] not in self.__class__.clients:
            self.__class__.clients[datas[1]]=[]
        if datas[0]=="sub":
            self.__class__.clients[datas[1]].append(writer)
        elif datas[0]=="pub":
            await self.pub(datas[1],datas[2])
            writer.close()
            await writer.wait_closed()
    

if __name__ == "__main__":
    broker = Broker()
    asyncio.run(broker.run())