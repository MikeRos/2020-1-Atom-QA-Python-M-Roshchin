import time

from paramiko import SSHClient, AutoAddPolicy, AuthenticationException, SSHException


class SSH:
    def __init__(self, **kwargs):
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.kwargs = kwargs

    def __enter__(self):
        kw = self.kwargs
        try:
            self.client.connect(
                hostname=kw.get('hostname'),
                port=int(kw.get('port', 2222)),
                username=kw.get('username'),
                password=kw.get('password'),
                look_for_keys=False,
                allow_agent=False
            )
        except AuthenticationException:
            print("Authentication failed, please verify your credentials")
        except SSHException as sshException:
            print(f"Could not establish SSH connection {sshException}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def exec_cmd(self, cmd):
        stdin, stdout, stderr = self.client.exec_command(cmd)
        data = stdout.read()
        data = data.decode()
        err = stderr.read()
        err = err.decode()
        if err:
            raise Exception(f'Err:{err}')
        return data

    def exec_root(self, cmd):
        stdin, stdout, _ = self.client.exec_command(f"sudo -S {cmd}")
        time.sleep(1)
        stdin.write("centos\n")
        stdin.flush()
        data = stdout.read()
        data = data.decode()
        return data
