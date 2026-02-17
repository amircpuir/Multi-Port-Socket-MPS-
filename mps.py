import asyncio
import struct
import os
import resource

def set_unlimited():
    try:
        resource.setrlimit(resource.RLIMIT_NOFILE, (1000000, 1000000))
    except Exception as e:
        print(f"\033[93m[!] Warning setting limits: {e}\033[0m")

BUFFER_SIZE = 65536

def print_header():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[94m" + "="*50)
    print("      CHANNEL: @Telhost1 | MODE: NATIVE SOCKET v1")
    print("="*50 + "\033[0m")

async def pipe(reader, writer):
    try:
        while True:
            data = await reader.read(BUFFER_SIZE)
            if not data:
                break
            writer.write(data)
            await writer.drain()
    except:
        pass
    finally:
        writer.close()

async def start_europe():
    print_header()
    tunnel_port = int(input("[?] Enter Tunnel Port (Europe, e.g., 26): "))

    async def handle_tunnel(reader, writer):
        remote_writer = None
        try:
            header = await reader.read(2)
            if not header: return
            target_port = struct.unpack('!H', header)[0]
            
            print(f"[*] Redirecting request to local port: {target_port}")
            
            remote_reader, remote_writer = await asyncio.open_connection('127.0.0.1', target_port)
            
            await asyncio.gather(
                pipe(reader, remote_writer),
                pipe(remote_reader, writer)
            )
        except:
            pass
        finally:
            if remote_writer: remote_writer.close()
            writer.close()

    server = await asyncio.start_server(handle_tunnel, '0.0.0.0', tunnel_port)
    print(f"\n🚀 Europe Tunnel is listening on port {tunnel_port}...")
    async with server:
        await server.serve_forever()

async def start_iran():
    print_header()
    ports_str = input("[?] Enter VPN Ports (e.g., 2091,8080): ")
    ports = [int(p.strip()) for p in ports_str.split(',')]
    e_ip = input("[?] Europe IP: ")
    e_port = int(input("[?] Europe Tunnel Port: "))

    async def handle_user(reader, writer, port):
        tunnel_writer = None
        try:
            tunnel_reader, tunnel_writer = await asyncio.open_connection(e_ip, e_port)
            
            tunnel_writer.write(struct.pack('!H', port))
            await tunnel_writer.drain()
            
            await asyncio.gather(
                pipe(reader, tunnel_writer),
                pipe(tunnel_reader, writer)
            )
        except:
            pass
        finally:
            if tunnel_writer: tunnel_writer.close()
            writer.close()

    for p in ports:
        await asyncio.start_server(lambda r, w, p=p: handle_user(r, w, p), '0.0.0.0', p)
        print(f"[+] User Listener Ready on port: {p}")

    print(f"\n🚀 Iran Bridge is active. Forwarding to {e_ip}:{e_port}")
    await asyncio.Future()

if __name__ == "__main__":
    set_unlimited()
    print("1) Europe Server\n2) Iran Server")
    choice = input("\nSelect: ")
    try:
        if choice == '1':
            asyncio.run(start_europe())
        elif choice == '2':
            asyncio.run(start_iran())
    except KeyboardInterrupt:
        sys.exit(0)
