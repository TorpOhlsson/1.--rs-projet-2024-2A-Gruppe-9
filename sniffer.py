import scapy.all as scapy
from datetime import datetime
import json 
import mysql.connector
from gpiozero import RGBLED
import binascii

red_pin = 22
green_pin = 27
blue_pin = 17

led = RGBLED(red=red_pin, green=green_pin, blue=blue_pin)
led.color = (0, 1, 0)

mydb = mysql.connector.connect(
    	host="xxx",
        user="xxx",
        password="xxx",
        database="xxx"
)

with open("/home/christian/sniffer/signatures.txt") as txt_file: 
    txt_data = txt_file.read() 
signatures = json.loads(txt_data)   

def save_log(src_ip, dst_ip,s_port, d_port, proto, raw):
	
	date_now = datetime.now()
	time = str(date_now.strftime("%d-%m-%Y %H:%M:%S"))
	status = "fine"

	#raw_seachable = str(raw.encode('UTF-8')).replace("\\x","")
	raw_seachable = str(raw).replace("\\x","").upper()

	for signature in signatures:
		if signature.upper() in raw_seachable:
			status = "infected"
			raw = "infected: " + signatures[signature] + raw	

	
	mycursor = mydb.cursor()

	sql = "INSERT INTO logs (src_ip, dst_ip, s_port, d_port, proto, packet, status, time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
	val = (src_ip, dst_ip,s_port, d_port, proto, str(raw), status, time)
	mycursor.execute(sql, val)

	mydb.commit()
	
	if status == "fine":
		led.color = (0, 1, 0)
	else:
		led.color = (1, 0, 0)


def process_packet(packet):
	
	src_ip = packet[0][1].src
	dst_ip = packet[0][1].dst
	proto = packet[0][1].proto
	#raw = packet.show(dump=True)
	raw = bytes(packet)
	try:
		s_port = packet[0][1].sport
		d_port = packet[0][1].dport		
	except:
		s_port = ""
		d_port = ""
	
	led.color = (0, 0, 1)
	
	save_log(src_ip, dst_ip, s_port, d_port, proto, raw)
		
ens6_traffic = scapy.sniff(iface="eth0", prn=process_packet, filter="ip")


