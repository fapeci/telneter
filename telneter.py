import telnetlib,time


def lexo(shtegu):
    with open(shtegu) as f:
        hosts = f.readlines()
    hosts = [x.strip() for x in hosts]
    f.close()
    return hosts

kredencialet = lexo('creds.txt')
hostat = lexo('hosts.txt')
komandat = lexo('commands.txt')

for host in hostat:
    f = open('precheck_' + host + '.txt', 'w')
    for komand in komandat:
        tn = telnetlib.Telnet(host, timeout=10)
        tn.set_debuglevel(0)
        tn.read_until("Password:")
        tn.write(kredencialet[0] + "\n")
        # EXEC Mode Prepping for command execution
        tn.write("enable\n")
        tn.read_until("Password:")
        tn.write(kredencialet[0] + "\n")
        tn.read_until("#")
        tn.write('terminal length 0' + "\n")
        tn.read_until("#")

        # Command Execution
        #for komand in komandat:
        tn.write(komand + "\n")
        time.sleep(3)
        tn.write('exit' + "\n")

        try:
            f.write(tn.read_all())
        except:
            tn.close()

        #tn.expect([re.compile("\w+#"),])
        #tn.write('exit' + "\n")
        print 'Start writing precheck for '+komand+' ... ' + host + ' to file'

        #print tn.read_all()

        tn.close()
        #print tn.read_all()
    f.close()
print '\n Finished ...'