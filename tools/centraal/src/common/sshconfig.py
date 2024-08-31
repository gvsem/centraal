from pathlib import Path
import subprocess
from os import listdir, mkdir
from os.path import isfile, isdir, join
import platform


class SshConfigManager:
    DIR_NAME = 'centraal'

    def __init__(self):
        self._init_environment()

    def get_key_filename_for_host(self, host: str):
        return str(self._ssh_centraal_path() / host)

    def add_key_if_not_exists(self, host: str, *, password=None):
        key = self.get_key_filename_for_host(host)
        if not isfile(key):
            subprocess.run(['ssh-keygen', '-t', 'ed25519',
                           '-N', password if password is not None else '', '-f', key], stdout=subprocess.DEVNULL,
                           stderr=subprocess.STDOUT)

        with open(str(self._ssh_config_filename()), 'a') as f:
            f.write('Host ' + host + '\n')
            f.write('HostName ' + host + '\n')
            f.write('User centraal\n')
            if platform.system() == 'Darwin':
                f.write('UseKeychain yes\n')
                f.write('AddKeysToAgent yes\n')
            f.write('IdentityFile ' + self.get_key_filename_for_host(host) + '\n')
            f.write('\n')

    def get_keys(self) -> set[str]:
        dir = self._ssh_centraal_path()
        return set([f for f in listdir(dir) if isfile(join(dir, f)) and not f.endswith('.pub')])

    def _init_environment(self):
        dir = str(self._ssh_centraal_path())
        config = self._ssh_config_filename()
        if not isdir(dir):
            mkdir(dir, mode=0o700)
            subprocess.run(['sudo', 'echo', 'Include ' + self.DIR_NAME +
                            '/config', ' >> ', str(Path.home() / '.ssh' / 'config')])
        if not isfile(config):
            Path(config).touch(mode=0o600)

    def _ssh_centraal_path(self) -> Path:
        return Path.home() / '.ssh' / self.DIR_NAME

    def _ssh_config_filename(self) -> str:
        return str(self._ssh_centraal_path() / 'config')

    def _ssh_key_for_host_filename(self, host: str) -> str:
        return str(self._ssh_centraal_path() / host)
