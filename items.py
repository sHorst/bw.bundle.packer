
pkg_pip = {
    'mako': {},
    # this needs to be installed, but pip does not state, that it is so use unless instead
    'setuptools': {
        'unless': 'pip list | grep setuptools',
    },
}

if node.has_bundle('apt'):
    files['/etc/apt/sources.list.d/hashicorp.list'] = {
        'content': 'deb [arch=amd64] https://apt.releases.hashicorp.com {release_name} main\n'.format(
            release_name=node.metadata.get(node.os).get('release_name')
        ),
        'content_type': 'text',
        'needs': ['file:/etc/apt/trusted.gpg.d/hashicorp.gpg', ],
        'triggers': ["action:force_update_apt_cache", ],
    }

    files['/etc/apt/trusted.gpg.d/hashicorp.gpg'] = {
        'content_type': 'binary',
    }

    pkg_apt = {
        'packer': {
            'needs': [
                'file:/etc/apt/trusted.gpg.d/hashicorp.gpg',
                'file:/etc/apt/sources.list.d/hashicorp.list',
            ]
        },
    }
