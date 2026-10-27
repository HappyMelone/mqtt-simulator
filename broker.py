import asyncio

class Broker:
    
    async def run(self):
        broker = await asyncio.start_server(self.gestisci_client,"127.0.0.1",8888)
        async with broker:
            await broker.serve_forever()

    async def sub(self,topic):
        pass

    async def pub(self,topic,msg):
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
        datas=dati.decode().split(":")
        if datas[0]=="sub":
            self.sub(datas[1])
        elif datas[0]=="pub":
            self.pub(datas[1],datas[2])
        print(f"Disconnesso: {ip}:{pn}")
        writer.close()
        await writer.wait_closed()
    

if __name__ == "__main__":
    broker = Broker()
    asyncio.run(broker.run())