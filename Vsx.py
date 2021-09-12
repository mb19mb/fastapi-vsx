#!/usr/bin/python
from datetime import datetime
from VsxTelnetClient import VsxTelnetClient
import sys, subprocess, imp


# noinspection PyInconsistentIndentation
class Vsx:
    path = "/home/pi/habridge/skripte/"
    logEnabled = True
    volumeTmpFile = ""
    vMax = 131
    vCurrent = 92
    vUpStepSize = 15
    vsxTelnetClient = None

    def __init__(self):
        self.__log("")
        self.__readConfigParams()
        self.vsxTelnetClient = VsxTelnetClient()

    def __readConfigParams(self):
        f = open(self.path + "config.sh", "r")
        for line in f:
            if line.startswith("VSX_VOL_TMP_FILE"):
                self.volumeTmpFile = line.split("=")[1]
            if line.startswith("MAXVOL"):
                self.vMax = line.split("=")[1]
        f.close()

    def __readCurrentVolume(self):
        # Aktuelle Lautstaerke ermitteln und in eine Dateischreiben
        subprocess.call(self.path + "lautstaerkestatus.sh")

        f = open(self.volumeTmpFile, "r")
        for line in f:
            if line.startswith("VOL"):
                self.vCurrent = int(line.lstrip("VOL").strip())
                break

        self.__vCurrentIsNumeric()
        self.__log("aktuelle Lautstaerke: " + str(self.vCurrent))

    def volume(self, percent):
        self.__log("volume")
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
        self.__log("ausschalten")
        # Status abfragen
        self.vsxTelnetClient.command("?P")
        currentState = self.vsxTelnetClient.getLastCommandResult()
        self.__log(currentState)

        if currentState == "PWR1":  # ist schon ausgeschalten
            self.__log("    ist schon ausgeschalten")
            return

        self.__log("PowerOff senden")
        self.vsxTelnetClient.command("PF") # PowerOff


    def einschalten(self):
        self.__log("einschalten")
        # Status abfragen
        self.vsxTelnetClient.command("?P")
        currentState = self.vsxTelnetClient.getLastCommandResult()
        self.__log(currentState)

        if currentState == "PWR0": # ist schon eingeschalten
            self.__log("    ist schon eingeschalten")
            return

        self.__log("PowerOn senden")
        self.vsxTelnetClient.command("PO") # PowerOn


    def lauter(self):
        self.__log("Lauter")
        # ermittelte Lautstaerke einlesen
        self.__readCurrentVolume()

        # Neue Lautstaerke setzen
        vnew = self.vCurrent + self.vUpStepSize

        # MAXWert ueberschritten? Beende
        if int(vnew) > int(self.vMax):
            self.__log("zulaut... mache nix")
            sys.exit()

        vnew = (str(vnew) + "VL").rjust(5, "0")
        self.__log("neuer Lautstaerkewerte: " + vnew + "\n")
        subprocess.call([self.path + "vsxExeCmd.sh", str(vnew)])

    def __vCurrentIsNumeric(self):
        # Konnte Lautstaerke nicht ermittelt werden, setzen wir Volume auf 92
        if str(self.vCurrent).isnumeric() == False:
            self.__log("vCurrent is not numceric. Adapt vCurrent...")
            self.vCurrent = 92

    def leiser(self):
        self.__log("leiser")

        self.vsxTelnetClient.command("?V")
        self.vCurrent = int(self.vsxTelnetClient.getLastCommandResult().replace("VOL", ""))

        vnew = self.vCurrent - self.vUpStepSize
        vnew = (str(vnew) + "VL").rjust(5, "0")
        self.__log("neuer Lautstaerkewerte: " + vnew + "\n")
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
