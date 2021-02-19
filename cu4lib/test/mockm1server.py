from cu4lib.server import CU4Server

class CU4TM1ServerMock(CU4Server):
    def __init__(self, *args, **kwargs):
        self._vals = {}

    def send_scpi(self, command):
        print("[MOCK] U4TM1ServerMock sending", command.strip())
        return str(self._reply_command(command.strip())) + "\r\n"

    def _reply_command(self, command):
        pcmd = self._parse_command(command)
        if pcmd["qtype"] == "get":
            return self._get_v(pcmd)
        if pcmd["qtype"] == "set":
            self._get_v(pcmd)
            self._vals[pcmd["fc"]] = pcmd["vars"]
            return "OK"

    def _get_v(self, pcmd):
        k = pcmd["fc"]
        if k not in self._vals:
            self._vals[k] = self._default(pcmd)
        return self._vals[k]
            

    def _parse_command(self, command):
        try:
            cmd, vs = command.split(" ")
        except:
            cmd = command
            vs = None
        cmdp = cmd.split(":")
        devn = int(cmdp[1][3:])
        cmd1 = cmdp[-1]
        if cmd1[-1] == "?":
            qtype = "get"
            cmd1 = cmd1[:-1]
            cmd = cmd[:-1]
        else:
            qtype = "set"
        try:
            chan = int(cmd1[-1:])
            cmd1 = cmd1[:-1]
        except:
            chan = None
        return {"fc": cmd, "devtype": cmdp[0], "devn": devn, "cmd": cmd1, "channel": chan, "vars": vs, "qtype": qtype} 
        
    def _default(self, pcmd):
        if pcmd["cmd"] == "TEMP":
            return 1.0 + pcmd["channel"]
        if pcmd["cmd"] == "CURR":
            return 2.0
        if pcmd["cmd"] == "VOLT":
            return 3.0
        if pcmd["cmd"] == "INIT":
            return "OK"
        raise Exception("Unknown command {}".format(pcmd) )

