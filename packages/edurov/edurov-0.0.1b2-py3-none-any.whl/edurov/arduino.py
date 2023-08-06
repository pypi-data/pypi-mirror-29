"""
Send motor commands to the arduino
"""

import signal

import Pyro4

from edurov.utils import detect_pi

if detect_pi():
    import serial

states = [0, 0, 0]
state = "000"
lastState = "000"


def start_arduino_coms(debug=False):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    if not debug:
        ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.05)
        ser.close()
        ser.open()
    with Pyro4.Proxy("PYRONAME:KeyManager") as keys:
        with Pyro4.Proxy("PYRONAME:ROVSyncer") as rov:
            while rov.run:
                if keys.state('a'):
                    states[1] = 1
                else:
                    states[1] = 0
                if keys.state('q'):
                    states[1] = 2
                else:
                    states[1] = 0
                if keys.state('w'):
                    states[0] = 1
                else:
                    states[0] = 0
                if keys.state('s'):
                    states[0] = 2
                else:
                    states[0] = 0
                if keys.state('e'):
                    states[2] = 2
                else:
                    states[0] = 0
                if keys.state('d'):
                    states[2] = 1
                else:
                    states[0] = 0

                state = ''.join([str(n) for n in states])
                if state != lastState:
                    lastState = state
                    if not debug:
                        ser.write(state)
                    else:
                        print(state)

    print('closing arduino coms')


if __name__ == '__main__':
    start_arduino_coms()
