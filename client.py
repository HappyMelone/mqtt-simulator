import sys,asyncio

async def main():
    if len(sys.argv)==2:                    #è un subscriber
        address=sys.argv[1]
        topic=sys.argv[2]
        reader,writer=await asyncio.open_connection(address,8888)
        writer.write(f"sub:{topic}".encode())
        while 1:
            data=reader.readline()
            print(data)
    elif len(sys.argv)==3:                  #è un publisher
        address=sys.argv[1]
        topic=sys.argv[2]        
        msg=sys.argv[3]
        reader,writer=await asyncio.open_connection(address,8888)
        writer.write(f"pub:{topic}:{msg}".encode())
    else:
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())