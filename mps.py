import asyncio
import struct
import os
import resource
import socket
import sys

# تنظیمات پیش‌فرض
DEFAULT_BUFFER = 65536

def set_unlimited():
    """افزایش محدودیت تعداد فایل‌های باز برای هندل کردن کانکشن‌های بالا"""
    try:
        resource.setrlimit(resource.RLIMIT_NOFILE, (1000000, 1000000))
    except Exception as e:
        # خطا در برخی سیستم‌عامل‌ها طبیعی است
        pass

def print_header():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[96m" + "="*50)
    print("       CHANNEL: @Telhost1 | MODE: STABLE SOCKET v2")
    print("="*50 + "\033[0m")

def configure_socket(sock):
    """تنظیمات سوکت برای پایداری و سرعت بیشتر"""
    try:
        # غیرفعال کردن الگوریتم Nagle برای کاهش تاخیر (Ping)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        # فعال‌سازی KeepAlive برای جلوگیری از قطع شدن اتصال‌های بیکار
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        
        # تنظیمات KeepAlive (بسته به سیستم عامل ممکن است متفاوت عمل کند)
        if hasattr(socket, 'TCP_KEEPIDLE'):
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
        if hasattr(socket, 'TCP_KEEPINTVL'):
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
        if hasattr(socket, 'TCP_KEEPCNT'):
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)
            
    except Exception:
        pass

async def pipe(reader, writer, buffer_size):
    """انتقال داده‌ها با مدیریت خطا و سایز بافر مشخص"""
    try:
        while True:
            # خواندن دیتا به اندازه MTU تعیین شده
            data = await reader.read(buffer_size)
            if not data:
                break
            writer.write(data)
            await writer.drain()
    except Exception:
        pass
    finally:
        # بستن کانکشن در صورت بروز هرگونه خطا
        try:
            writer.close()
        except:
            pass

async def start_europe():
    print_header()
    tunnel_port = int(input("\033[93m[?] Enter Tunnel Port (Europe, e.g., 443): \033[0m"))
    mtu_size = input("\033[93m[?] Enter MTU Size (Default 1500, Recommended 1400): \033[0m")
    
    # تنظیم بافر بر اساس MTU
    BUFFER_SIZE = int(mtu_size) if mtu_size.strip() else 1500
    print(f"[*] Buffer set to: {BUFFER_SIZE} bytes")

    async def handle_tunnel(reader, writer):
        # اعمال تنظیمات سوکت روی کانکشن ورودی
        sock = writer.get_extra_info('socket')
        if sock: configure_socket(sock)

        remote_writer = None
        try:
            # خواندن هدر برای پیدا کردن پورت مقصد
            header = await reader.read(2)
            if not header: return
            target_port = struct.unpack('!H', header)[0]
            
            # اتصال به پورت لوکال (مثلا پورت پنل)
            remote_reader, remote_writer = await asyncio.open_connection('127.0.0.1', target_port)
            
            # تنظیم سوکت مقصد
            rsock = remote_writer.get_extra_info('socket')
            if rsock: configure_socket(rsock)

            # شروع تبادل دو طرفه
            await asyncio.gather(
                pipe(reader, remote_writer, BUFFER_SIZE),
                pipe(remote_reader, writer, BUFFER_SIZE)
            )
        except Exception as e:
            pass
        finally:
            if remote_writer: remote_writer.close()
            writer.close()

    server = await asyncio.start_server(handle_tunnel, '0.0.0.0', tunnel_port)
    print(f"\n\033[92m🚀 Europe Server Listening on port {tunnel_port} with optimized MTU...\033[0m")
    async with server:
        await server.serve_forever()

async def start_iran():
    print_header()
    ports_str = input("\033[93m[?] Enter VPN Ports (e.g., 2091,8080): \033[0m")
    ports = [int(p.strip()) for p in ports_str.split(',')]
    
    e_ip = input("\033[93m[?] Europe IP: \033[0m")
    e_port = int(input("\033[93m[?] Europe Tunnel Port: \033[0m"))
    
    mtu_size = input("\033[93m[?] Enter MTU Size (Recommended for Iran: 1300-1400): \033[0m")
    BUFFER_SIZE = int(mtu_size) if mtu_size.strip() else 1400
    print(f"[*] Buffer set to: {BUFFER_SIZE} bytes")

    async def handle_user(reader, writer, target_port):
        # تنظیم سوکت کاربر
        sock = writer.get_extra_info('socket')
        if sock: configure_socket(sock)
        
        tunnel_writer = None
        try:
            # اتصال به سرور خارج
            tunnel_reader, tunnel_writer = await asyncio.open_connection(e_ip, e_port)
            
            # تنظیم سوکت تونل
            tsock = tunnel_writer.get_extra_info('socket')
            if tsock: configure_socket(tsock)

            # ارسال پورت مقصد به سرور خارج
            tunnel_writer.write(struct.pack('!H', target_port))
            await tunnel_writer.drain()
            
            # تبادل داده
            await asyncio.gather(
                pipe(reader, tunnel_writer, BUFFER_SIZE),
                pipe(tunnel_reader, writer, BUFFER_SIZE)
            )
        except Exception:
            # در صورت قطع شدن اینترنت یا خطا، کانکشن بسته می‌شود
            pass 
        finally:
            if tunnel_writer: tunnel_writer.close()
            writer.close()

    # راه‌اندازی لیسنر برای همه پورت‌های وارد شده
    for p in ports:
        try:
            server = await asyncio.start_server(lambda r, w, p=p: handle_user(r, w, p), '0.0.0.0', p)
            print(f"\033[92m[+] Listening on port: {p}\033[0m")
            asyncio.create_task(server.serve_forever())
        except Exception as e:
            print(f"\033[91m[!] Failed to bind port {p}: {e}\033[0m")

    print(f"\n\033[92m🚀 Iran Bridge Active. Forwarding > {e_ip}:{e_port}\033[0m")
    print("\033[90mPress Ctrl+C to stop.\033[0m")
    
    # نگه‌داشتن برنامه
    await asyncio.Event().wait()

if __name__ == "__main__":
    set_unlimited()
    try:
        print_header()
        print("1) Europe Server (Destination)")
        print("2) Iran Server (Bridge)")
        choice = input("\n\033[96mSelect Option: \033[0m")
        
        if choice == '1':
            asyncio.run(start_europe())
        elif choice == '2':
            asyncio.run(start_iran())
        else:
            print("Invalid Choice!")
    except KeyboardInterrupt:
        print("\n\033[91m[!] Stopping...\033[0m")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
