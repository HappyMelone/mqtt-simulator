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
        type=dati.decode().strip()
        if type=="sub":
            topic=await reader.readline()
            if not dati:
                print(f"Disconnesso: {ip}:{pn}")
                writer.close()
                await writer.wait_closed()
                return
            while 1:
                lettura=asyncio.create_task(reader.readline())
                altro=asyncio.create_task(self.sub(topic))   # resto del programma
                done,pending=await asyncio.wait({lettura,altro},return_when=asyncio.FIRST_COMPLETED)
                for t in pending:
                    t.cancel()
                if lettura in done and not lettura.result():
                    break
        """
        while 1:
            dati = await reader.readline()
            if not dati:
                break
            testo = dati.decode().strip()
            print(f"{ip}:{pn} ha scritto: {testo}")
    
            await asyncio.sleep(0)
            risposta = testo.upper() + "\n"
            writer.write(risposta.encode())
            await writer.drain()
        """
        print(f"Disconnesso: {ip}:{pn}")
        writer.close()
        await writer.wait_closed()
    

if __name__ == "__main__":
    broker = Broker()
    asyncio.run(broker.run())