import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_package_is_installed(host):
    if (host.system_info.distribution.lower() == 'redhat'
            or host.system_info.distribution.lower() == 'centos'):
        os_r = host.system_info.release
        if os_r.startswith('8'):
            package_centos8 = host.package('dnf-automatic')
            assert package_centos8.is_installed
        else:
            package_centos = host.package('yum-cron')
            assert package_centos.is_installed
    else:
        package = host.package('unattended-upgrades')
        assert package.is_installed
        package2 = host.package('bsd-mailx')
        assert package2.is_installed


def test_service_is_enabled_and_running(host):
    if ((host.system_info.distribution.lower() == 'redhat'
            or host.system_info.distribution.lower() == 'centos')
            and host.system_info.release.startswith('8')):
        service = host.service('dnf-automatic.timer')
        assert service.is_running
        assert service.is_enabled
    else:
        service = host.service('apt-daily-upgrade.timer')
        assert service.is_running
        assert service.is_enabled


def test_file_content(host):
    if (host.system_info.distribution.lower() == 'redhat'
            or host.system_info.distribution.lower() == 'centos'):
        os_r = host.system_info.release
        if os_r.startswith('6'):
            conf_file = host.file('/etc/sysconfig/yum-cron')
            assert conf_file.contains("CHECK_FIRST=no")
        elif os_r.startswith('7'):
            conf_file = host.file('/etc/yum/yum-cron.conf')
            assert conf_file.contains("download_updates = yes")
        else:
            conf_file = host.file('/etc/dnf/automatic.conf')
            assert conf_file.contains("download_updates = yes")
    else:
        conf_file = host.file('/etc/apt/apt.conf.d/50unattended-upgrades')
        assert conf_file.contains("Unattended-Upgrade::Allowed-Origins {")
