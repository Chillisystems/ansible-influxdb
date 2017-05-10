import pytest
from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner('.molecule/ansible_inventory').get_hosts('all')


@pytest.mark.parametrize("name, version", [
    ('influxdb', '1.2.2')
])
def test_packages(Package, name, version):
    pkg = Package(name)
    assert pkg.is_installed
    assert pkg.version.startswith(version)


@pytest.mark.parametrize('service_name', [
    ('influxdb'),
])
def test_kafka_service_enabled(Service, service_name):
    s = Service(service_name)

    assert s.is_running
    assert s.is_enabled


@pytest.mark.parametrize('service_url', [
    ('tcp://:::8086'),
    ('tcp://:::8088'),
])
def test_kafka_is_running(Socket, service_url):
    s = Socket(service_url)

    assert s.is_listening
