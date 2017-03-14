import socket
import cv2
import commands
import numpy as np

def get_port():
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(('', 0))
	val = sock.getsockname()[1]
	sock.close()
	return val

def main():

	udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	ip = commands.getoutput("hostname -I")[:13]
	port = get_port()

	print 'IP of the server : ', ip
	print 'Port used by server : ', port

	udp_sock.bind((ip, port))
	tcp_sock.bind((ip, port))
	tcp_sock.listen(port)

	conn, addr = tcp_sock.accept()
	buf = int(conn.recv(1024))

	f_name = conn.getpeername()[0]+".avi"

	fourcc = cv2.cv.CV_FOURCC('X', 'V', 'I', 'D')
	out = cv2.VideoWriter(f_name, fourcc, 20.0, (320, 240))

	while(True):

		data, addr = udp_sock.recvfrom(1024*buf)
		
		nparr = np.fromstring(data, np.uint8)
		frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
		
		out.write(frame)

		cv2.imshow('Frame',frame)

		if(cv2.waitKey(1) & 0xFF == ord('q')):
			break

	out.release()
	cv2.destroyAllWindows()
	udp_sock.close()
	tcp_sock.close()

if __name__ == "__main__":
	main()