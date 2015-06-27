import socket
import sys
import time

#docs:
# http://www.limitlessled.com/dev/

host = "10.10.10.255" #broadcast ip for my subnet
port = 8899

#            all 1   2   3   4
group_on  = [66, 69, 71, 73, 75]
group_off = [65, 70, 72, 74, 76]
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((host, port))
except socket.error:
    print ("Failed to create socket")
    sys.exit()

def main():
    if len(sys.argv) == 1:
        print("arugments: [group] [command] [value]")
        print("0 color 45   set color value for group all to 45")
    else:
        g = int(sys.argv[1])
        command = sys.argv[2]
        
        if 0 <= g <= 4:
            if command == 'color':
                color(group_on[g], int(sys.argv[3]))
            if command == 'brightness':
                brightness(group_on[g], int(sys.argv[3]))
            if command == 'on':
                s.send(bytearray([group_on[g],0]))                
            if command == 'off':
                s.send(bytearray([group_off[g],0]))
        else:
            print("group must be 0-4 (0 send command to all)")

def net_send(group, mode, value):
    try:
        s.send(bytearray([group]))
        time.sleep(0.1)
        s.send(bytearray([mode, value, 85]))
    except socket.error as e:
        print ('Error Code : ' + str(e[0]) + ' Message ' + e[1])
        sys.exit()

def brightness(group, brightness):
    """set brightness 2-27"""
    net_send(group, 78, brightness)

def color(group, color):
    """set color 0-255"""
    net_send(group, 64, color)

if __name__ == "__main__":
    main()