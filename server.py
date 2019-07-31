import argparse
import sys, signal

from PyQt5.QtCore import QCoreApplication

from server.serverQt import ServerQt
from server.serverSocket import ServerSocket


if __name__ == '__main__':

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Argument Parser
    parser = argparse.ArgumentParser(
        description="Run a TCP Server waiting for client to connect and send data")
    parser.add_argument("--HOST", type=str, default="localhost",
                        help="host IP")
    parser.add_argument("--PORT", type=int, default=8493,
                        help="commmunication port")
    parser.add_argument("--socket",action="store_true", 
                        help="use socket instead of QTCPSocket (deprecated)")

    args = parser.parse_args()

    if args.socket:
        ServerSocket(args.HOST, args.PORT)
    else:
        app = QCoreApplication(sys.argv)
        form = ServerQt(app, args.HOST, args.PORT)
        sys.exit(app.exec_())
