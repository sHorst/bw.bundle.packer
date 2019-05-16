PACKER_VER = '1.2.4'
PACKER_SUM = '258d1baa23498932baede9b40f2eca4ac363b86b32487b36f48f5102630e9fbb'


directories = {
    '/opt/packer': {
        'owner': 'root',
        'group': 'root',
        'mode': "0751",
    },
}

downloads = {
    '/opt/packer/packer_{0}.zip'.format(PACKER_VER): {
        'url': 'https://releases.hashicorp.com/packer/{0}/packer_{0}_linux_amd64.zip'.format(PACKER_VER),
        'sha256': PACKER_SUM,
        'needs': ['directory:/opt/restic', 'pkg_apt:ca-certificates'],
        'unless': 'test -f /opt/packer/packer-{}'.format(PACKER_VER),
    }
}

pkg_pip = {
    'mako': {},
    # this needs to be installed, but pip does not state, that it is so use unless instead
    'setuptools': {
        'unless': 'pip list | grep setuptools',
    },
}

actions = {
    'install_packer': {
        'command': 'cd /opt/packer && '
                   'unzip -p packer_{0}.zip packer > packer-{0} && '
                   'rm -f packer_{0}.zip &&'
                   'chmod +x packer-{0} && '
                   'ln -sf /opt/packer/packer-{0} /usr/local/sbin/packer'.format(PACKER_VER),
        'unless': 'test -x /opt/packer/packer-{0} && '
                  'cmp /usr/local/sbin/packer /opt/packer/packer-{0}'.format(PACKER_VER),
        'needs': ['pkg_apt:unzip', 'download:/opt/packer/packer_{0}.zip'.format(PACKER_VER)]
    }
}
