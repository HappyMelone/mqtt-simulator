import sys,asyncio

"""
python client.py 127.0.0.1 <topic> <msg>?
"""

async def main():
    if len(sys.argv)==3:                    #è un subscriber
        address=sys.argv[1]
        topic=sys.argv[2]
        reader,writer=await asyncio.open_connection(address,8888)
        writer.write(f"sub:{topic}\n".encode())
        await writer.drain()
        while 1:
            data=await reader.readline()
            if not data:
                break
            print(data.decode().rstrip())
    elif len(sys.argv)>=4:                  #è un publisher
        address=sys.argv[1]
        topic=sys.argv[2]
        msg=[]
        for indice in range(len(sys.argv)):
            if indice<3:
                continue
            msg.append(sys.argv[indice])
        msg=" ".join(msg)
        reader,writer=await asyncio.open_connection(address,8888)
        writer.write(f"pub:{topic}:{msg}\n".encode())
        await writer.drain()
    else:
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())