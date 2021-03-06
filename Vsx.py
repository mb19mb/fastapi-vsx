#!/usr/bin/python
from datetime import datetime
from VsxTelnetClient import VsxTelnetClient
import sys, subprocess, imp

# noinspection PyInconsistentIndentation
class Vsx:
    logEnabled = True
    vInit = 100
    vMax = 131
    vCurrent = 92
    vUpStepSize = 15
    vsxTelnetClient = None

    def __init__(self):
        self.__log("")
        self.vsxTelnetClient = VsxTelnetClient()

    def __readCurrentVolume(self):
        self.vsxTelnetClient.command("?V")
        self.vCurrent = int(self.vsxTelnetClient.getLastCommandResult().replace("VOL", ""))
        self.__checkCurrentIsNumeric()
        self.__log("aktuelle Lautstaerke: " + str(self.vCurrent))

    def umschalten(self, channel):
        self.__log("umschalten("+channel+")")
        self.vsxTelnetClient.command("?F")
        currentChannel= self.vsxTelnetClient.getLastCommandResult()
        if channel == "CD":
            if currentChannel != "01FN":
                vnew = (str(self.vInit) + "VL").rjust(5, "0")
                self.vsxTelnetClient.command(vnew)
                self.__log("    Volume setzen")
                self.vsxTelnetClient.command("01FN")
                self.__log("    Kanal wechseln")
        if channel == "PS3":
            if currentChannel != "25FN":
                self.vsxTelnetClient.command("071VL")
                self.__log("    Volume setzen")
                self.vsxTelnetClient.command("25FN")
                self.__log("    Kanal wechseln")
        if channel == "TV":
            if currentChannel != "06FN":
                self.vsxTelnetClient.command("071VL")
                self.__log("    Volume setzen")
                self.vsxTelnetClient.command("06FN")
                self.__log("    Kanal wechseln")
        
    def volume(self, percent):
        self.__log("volume()")
        self.__log(str(percent))
        vnew = int(round(self.vMax / 100 * percent))

        if int(vnew) > int(self.vMax): # MAXWert ueberschritten? Beende
            self.__log("    zulaut... mache nix")
            sys.exit()

        vnew = (str(vnew) + "VL").rjust(5, "0")
        self.__log("    neuer Lautstaerkewerte: " + vnew + "\n")
        self.vsxTelnetClient.command(vnew)
        #subprocess.call([self.path + "vsxExeCmd.sh", str(vnew)])

    def ausschalten(self):
        self.__log("ausschalten()")
        # Status abfragen
        self.vsxTelnetClient.command("?P")
        currentState = self.vsxTelnetClient.getLastCommandResult()
        self.__log(currentState)

        if currentState == "PWR1":  # ist schon ausgeschalten
            self.__log("    ist schon ausgeschalten")
            return

        self.__log("    PowerOff senden")
        self.vsxTelnetClient.command("PF") # PowerOff


    def einschalten(self):
        self.__log("einschalten()")
        # Status abfragen
        self.vsxTelnetClient.command("?P")
        currentState = self.vsxTelnetClient.getLastCommandResult()
        self.__log(currentState)

        if currentState == "PWR0": # ist schon eingeschalten
            self.__log("    ist schon eingeschalten")
            return

        self.__log("    PowerOn senden")
        self.vsxTelnetClient.command("PO") # PowerOn


    def lauter(self):
        self.__log("lauter()")
        self.__readCurrentVolume()

        vnew = self.vCurrent + self.vUpStepSize # Neue Lautstaerke setzen

        # MAXWert ueberschritten? Beende
        if int(vnew) > int(self.vMax):
            self.__log("    zulaut... mache nix")
            return

        vnew = (str(vnew) + "VL").rjust(5, "0")
        self.__log("    neuer Lautstaerkewerte: " + vnew + "\n")
        self.vsxTelnetClient.command(str(vnew))


    def __checkCurrentIsNumeric(self):
        # Konnte Lautstaerke nicht ermittelt werden, setzen wir Volume auf 92
        if str(self.vCurrent).isnumeric() == False:
            self.__log("    vCurrent is not numceric. Adapt vCurrent...")
            self.vCurrent = 92

    def leiser(self):
        self.__log("leiser()")

        self.__readCurrentVolume()

        vnew = self.vCurrent - self.vUpStepSize
        vnew = (str(vnew) + "VL").rjust(5, "0")
        self.__log("    neuer Lautstaerkewerte: " + vnew + "\n")
        self.vsxTelnetClient.command(vnew)


    def __log(self, msg):
        if self.logEnabled == False:
            return
        f = open("/tmp/vsx.log", "a+")
        logMsg = msg
        if msg != "":
            logMsg = str(datetime.now()) + ": " + msg
        logMsg += "\n"
        f.write(logMsg)
        f.close()
