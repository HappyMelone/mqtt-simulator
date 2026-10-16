import asyncio

class Broker:

    def __init__(self):
        pass
    
    async def run(self):
        broker = await asyncio.start_server(self.gestisci_client,"127.0.0.1",8888)
        async with broker:
            await broker.serve_forever()

    async def gestisci_client(self,reader,writer):
        print("Ciao")
        ip,pn = writer.get_extra_info("peername")
        print(f"Connesso: {ip}:{pn}")
        while True:
            dati = await reader.readline()
            if not dati:
                break
    
            testo = dati.decode().strip()
            print(f"{ip}:{pn} ha scritto: {testo}")
    
            await asyncio.sleep(10)
            #time.sleep(5)
            risposta = testo.upper() + "\n"
            writer.write(risposta.encode())
            await writer.drain()
    
        print(f"Disconnesso: {ip}:{pn}")
        writer.close()
        await writer.wait_closed()

if __name__ == "__main__":
    broker = Broker()
    asyncio.run(broker.run())