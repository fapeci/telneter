import telnetlib,time


def readfile(path):
    with open(path) as f:
        hosts = f.readlines()
    hosts = [x.strip() for x in hosts]
    f.close()
    return hosts

credentials = readfile('creds.txt')
hosts = readfile('hosts.txt')
commands = readfile('commands.txt')

for host in hosts:
    f = open('precheck_' + host + '.txt', 'w')
    for command in commands:
        tn = telnetlib.Telnet(host, timeout=10)
        tn.set_debuglevel(0)
        password = credentials[0]

        # EXEC Mode Prepping for IOS command execution
        tn.read_until("Password:")
        tn.write(password + "\n")
        tn.write("enable\n")
        tn.read_until("Password:")
        tn.write(password + "\n")
        tn.read_until("#")
        tn.write('terminal length 0' + "\n")
        tn.read_until("#")

        # Command Execution
        tn.write(command + "\n")
        time.sleep(3)
        tn.write('exit' + "\n")
        try:
            f.write(tn.read_all())
        except:
            tn.close()
        print 'Start writing precheck for '+command+' ... '  + ' to file precheck_'+ host + '.txt'
        tn.close()
    f.close()
print '\n Finished ...'