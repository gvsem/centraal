import argparse
import getpass
import os.path
import sys
import paramiko
from paramiko.ed25519key import Ed25519Key
import subprocess
from common.sshconfig import SshConfigManager
from common.console import ssh_run_cmds

parser = argparse.ArgumentParser(
    description='Zero-day initial centraal master cluster setup.')
parser.add_argument('tool', choices=['master'])
parser.add_argument('subtool', choices=['init'])
parser.add_argument(
    'host',
    action='store',
    help='centraal master hostname (e.g. centraal.ru, or 8.8.8.8)')
parser.add_argument(
    '-u',
    '--user',
    dest='user',
    action='store',
    required=False,
    default='root',
    help='ssh sudoed username (default: root)')
parser.add_argument(
    '-p',
    '--port',
    dest='port',
    action='store',
    required=False,
    default=22,
    help='initial ssh port (default: 22)',
    choices=range(
        1,
         65536))
parser.add_argument(
    '--no-passphrase',
    dest='no_passphrase',
    action='store_true',
    required=False,
    default=False,
    help='do not encrypt ssh private key')
parser.add_argument(
    '--ed25519-key-file',
    dest='private_key_file',
    action='store',
    required=False,
    help='use specific private key authentication instead of password')

args = parser.parse_args()

host = args.host
port = args.port
user = args.user
hostname = user + '@' + host + ':' + str(port)
private_key_file = None
ssh_key_password = None

if args.private_key_file is not None and not os.path.isfile(
        args.private_key_file):
    print('ssh private key does not exist: ' +
          private_key_file, file=sys.stderr)
    sys.exit(1)

ssh_config_manager = SshConfigManager()

if args.private_key_file is None:
    private_key_file = ssh_config_manager.get_key_filename_for_host(host)
    if host not in ssh_config_manager.get_keys():
        print('Generating new ssh key pair for ' + host)
        if not args.no_passphrase:
            ssh_key_password = getpass.getpass(
                prompt='Enter password to encrypt ssh key for ' + host)
        ssh_config_manager.add_key_if_not_exists(
            host, password=ssh_key_password)
        subprocess.run(['ssh-copy-id', '-i', private_key_file, '-p', str(port),
                        user + '@' + host])


client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

if ssh_key_password is None and not args.no_passphrase:
    ssh_key_password = getpass.getpass(
        prompt='Enter password to decrypt ssh key for ' + host)

print(private_key_file)

client.connect(host,
               username=user,
               pkey=Ed25519Key.from_private_key_file(
                   private_key_file, ssh_key_password),
               port=port)

ssh_run_cmds(client, [
    'id -u centraal &>/dev/null || adduser centraal --disabled-password --gecos ""',
    'usermod -aG sudo centraal',
    'mkdir -p /home/centraal/.ssh',
    'cp ~/.ssh/authorized_keys /home/centraal/.ssh/authorized_keys',
    'echo -e "ChallengeResponseAuthentication no \nPasswordAuthentication no \nUsePAM no \nPermitRootLogin no" > /etc/ssh/sshd_config.d/disable_root_login.conf',
    'systemctl reload ssh'
])

client.close()
