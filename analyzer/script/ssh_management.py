from socket import error as socket_error

from fabric import Connection
from invoke import Responder
from paramiko.ssh_exception import AuthenticationException


class Host(object):
    def __init__(self,
                 host_ip,
                 username,
                 password,
                 
                 ):
        self.host_ip = host_ip
        self.username = username
        self.password = password
        

    def _get_connection(self):
        return Connection(host=self.host_ip, user=self.username,
                          port=22,
                          connect_kwargs={"password": self.password},
                          )

    def run_command(self, command):
        try:
            with self._get_connection() as connection:
                sudopass = Responder(
                    pattern=r'\[sudo\] password',
                    response='1234\n',
                )
                result = connection.run(command, warn=True, pty=True, watchers=[sudopass])
                return result
        except (socket_error, AuthenticationException) as exc:
            self._raise_authentication_err(exc)

        if result.failed:
            raise Exception(
                'The command `{0}` on host {1} failed with the error: '
                '{2}'.format(command, self.host_ip, str(result.stderr)))

    def get_pcap(self, remote_path, local_path):
        try:
            with self._get_connection() as connection:
                print('Copying {0} to {1} on host {2}'.format(
                    remote_path, local_path, self.host_ip))
                connection.get(remote_path, local_path)
        except (socket_error, AuthenticationException) as exc:
            self._raise_authentication_err(exc)

    def put_script(self, remote_path, local_path):
        try:
            with self._get_connection() as connection:
                print('Copying {0} to {1} on host {2}'.format(
                    remote_path, local_path, self.host_ip))
                connection.put(remote_path, local_path)
        except (socket_error, AuthenticationException) as exc:
            self._raise_authentication_err(exc)

    def _raise_authentication_err(self, exc):
        raise Exception(
            "SSH: could not connect to {host} "
            "(username: {user}, key: {password}): {exc}".format(
                host=self.host_ip, user=self.username,
                password=self.password, exc=exc))
