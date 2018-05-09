from pythonosc import dispatcher
import threading

"""OSC Servers that receive UDP packets and invoke handlers accordingly.
Use like this:"""

dispatcher = dispatcher.Dispatcher()
# This will print all parameters to stdout.
dispatcher.map("/bpm", print)
#server = ForkingOSCUDPServer((ip, port), dispatcher)
#server.serve_forever()
#or run the server on its own thread:
server = ForkingOSCUDPServer((ip, port), dispatcher)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.start()
...
server.shutdown()