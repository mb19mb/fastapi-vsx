import getpass, telnetlib, time

class VsxTelnetClient:
    debugLevel = 0
    tn = None
    telnetHost = "192.168.20.208"
    telnetPort = 8102
    currentCmd = ""
    output = ""
    outList = []

    def __init__(self):
        self.tn = telnetlib.Telnet(None)
        self.tn.set_debuglevel(self.debugLevel)

    def command(self, cmd):
        self.currentCmd = cmd
        self.__openTelnet()
        self.outList = []
        self.output = self.tn.read_eager()
        self.outList.append(self.output)
        self.tn.write(cmd.encode('ascii') + "\r\n".encode('ascii'))
        time.sleep(0.5)
        done = False
        value = None
        while not done:
            value = self.tn.read_eager()
            self.output += value
            if value == b"" or value == "":
                done = True

        self.outList.append(self.output)
        self.__closeTelnet()


    def getLastCommandResult(self):
        print("-----")
        return self.output
        # r = ""
        # for s in self.outList:
        #     r += s
        # print(r)
        # return r

    def __printLastCommandResult(self):
        print(self.currentCmd)
        print(self.outList)
        print("\n\n")

    def __openTelnet(self):
        self.tn.open(self.telnetHost, self.telnetPort)

    def __closeTelnet(self):
        self.tn.close()


if __name__ == "__main__":
    print("?")
    v = VsxTelnetClient()
    print(v)
    #v.command("?V")
    v.command("?P")
    print(v.getLastCommandResult())
