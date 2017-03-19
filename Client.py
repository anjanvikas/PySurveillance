import socket
import cv
import cv2
import sys
import numpy as np
import zlib

def main():

	ip = raw_input("Enter the IP address of the server : ")
	port = input("Enter the socket given by the server : ")

	udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	tcp_sock.connect((ip, port))
	
	cap = cv2.VideoCapture(0)
	cap.set(cv.CV_CAP_PROP_FRAME_WIDTH,320)
	cap.set(cv.CV_CAP_PROP_FRAME_HEIGHT,240)

	while(True):
		
		ret, frame = cap.read()
		
		buf = cv2.imencode('.jpg', frame)[1].tostring()
		message = str(sys.getsizeof(buf))
		buf = zlib.compress(buf, 9)
		try:
			tcp_sock.send(message)
			udp_sock.sendto(buf, (ip, port))
		except socket.error:
			break	
	
		if(cv2.waitKey(1) & 0xFF == ord('q')):
			break
			

	cap.release()
	cv2.destroyAllWindows()
	udp_sock.close()
	tcp_sock.close()

if __name__ == "__main__":
	main()
