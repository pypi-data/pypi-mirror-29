from unittest import TestCase

from mock import Mock
from mock import MagicMock

from cloudshell.cp.aws.domain.services.ec2.instance import InstanceService


class TestInstanceService(TestCase):
    def setUp(self):
        self.tag_service = Mock()
        self.instance_waiter = Mock()
        self.ec2_session = Mock()
        self.ec2_client = Mock()
        self.name = 'name'
        self.reservation_id = 'res_id'
        self.instance = MagicMock()
        self.instance.instance_id = 'id'
        self.default_tags = ['tag1', 'tag2']
        self.tag_service.get_default_tags = Mock(return_value=self.default_tags)
        self.ec2_session.create_instances = Mock(return_value=[self.instance])
        self.ec2_session.Instance = Mock(return_value=self.instance)
        self.instance_service = InstanceService(self.tag_service, self.instance_waiter)

    #@Mock.Patch('cloudshell.cp.aws.domain.services.ec2.instance.create_instances')
    def test_create_instance(self):
        ami_dep = Mock()
        cancellation_context = Mock()
        new_instance = Mock()
        new_instance.instance_id='id'
        self.ec2_session.create_instances = Mock(return_value=[new_instance])

        res = self.instance_service.create_instance(ec2_session=self.ec2_session,
                                                    name=self.name,
                                                    reservation=self.reservation_id,
                                                    ami_deployment_info=ami_dep,
                                                    ec2_client=self.ec2_client,
                                                    wait_for_status_check=False,
                                                    cancellation_context=cancellation_context,
                                                    logger=Mock())

        self.assertTrue(self.ec2_session.create_instances.called_with(ami_dep.aws_ami_id,
                                                                      ami_dep.min_count,
                                                                      ami_dep.max_count,
                                                                      ami_dep.instance_type,
                                                                      ami_dep.aws.key,
                                                                      ami_dep.block_device_mappings,
                                                                      [
                                                                          {
                                                                              'SubnetId': ami_dep.subnet_id,
                                                                              'DeviceIndex': 0,
                                                                              'Groupd': ami_dep.security_group_ids
                                                                          }
                                                                      ]))

        self.instance_waiter.wait.assert_called_once_with(instance=new_instance,
                                                          state=self.instance_waiter.RUNNING,
                                                          cancellation_context=cancellation_context)
        self.assertTrue(self.tag_service.get_default_tags.called_with(self.name + ' ' + self.reservation_id,
                                                                      self.reservation_id))
        self.assertTrue(self.tag_service.set_ec2_resource_tags.called_with(self.instance, self.default_tags))
        self.assertTrue(new_instance.load.called)
        self.assertEqual(new_instance, res)

    def test_get_instance_by_id(self):
        res = self.instance_service.get_instance_by_id(self.ec2_session, 'id')
        self.assertTrue(self.ec2_session.Instance.called_with('id'))
        self.assertIsNotNone(res)

    def test_get_active_instance_by_id_raise_exception_if_vm_terminated(self):
        """Check that method will raise exception if VM was terminated on the AWS"""
        self.instance.state = {'Name': 'terminated'}
        with self.assertRaises(Exception):
            self.instance_service.get_active_instance_by_id(self.ec2_session, 'id')

    def test_get_active_instance_by_id_raise_exception_if_no_vm(self):
        """Check that method will raise exception if VM was removed from the AWS"""
        self.ec2_session.Instance = Mock(return_value=None)
        with self.assertRaises(Exception):
            self.instance_service.get_active_instance_by_id(self.ec2_session, 'id')

    def test_find_and_release_elastic_address(self):
        # arrange
        ec2_session = Mock()
        elastic_ip = "xxx"
        vpc_address = Mock()
        ec2_session.vpc_addresses.filter = Mock(return_value=[vpc_address])

        # act
        self.instance_service.find_and_release_elastic_address(ec2_session=ec2_session, elastic_ip=elastic_ip)

        # assert
        ec2_session.vpc_addresses.filter.assert_called_once_with(PublicIps=[elastic_ip])
        vpc_address.release.assert_called_once()

    def test_find_and_release_elastic_address_failed_to_find_ip(self):
        # arrange
        ec2_session = Mock()
        elastic_ip = "xxx"
        ec2_session.vpc_addresses.filter = Mock(return_value=[])

        # act & assert
        with self.assertRaisesRegexp(ValueError, "Failed to find elastic ip xxx"):
            self.instance_service.find_and_release_elastic_address(ec2_session=ec2_session, elastic_ip=elastic_ip)

    def test_terminate_instance(self):
        self.instance_waiter.multi_wait = Mock(return_value=[self.instance])
        res = self.instance_service.terminate_instance(self.instance)

        self.assertTrue(self.instance.terminate.called)
        self.assertTrue(self.instance_waiter.multi_wait.called_with([self.instance], 'terminated'))
        self.assertIsNotNone(res)

    def test_terminate_instances(self):
        instances = [Mock(), Mock()]
        res = self.instance_service.terminate_instances(instances)

        self.assertTrue(instances[0].terminate.called)
        self.assertTrue(instances[1].terminate.called)
        self.assertTrue(self.instance_waiter.multi_wait.called_with([self.instance], 'terminated'))
        self.assertIsNotNone(res)

    def test_release_elastic_address(self):
        vpc_address = Mock()
        res = self.instance_service.release_elastic_address(vpc_address)
        self.assertTrue(vpc_address.release.called)

    def test_allocate_elastic_address(self):
        ec2_client = Mock()
        result={'PublicIp': 'string'}
        ec2_client.allocate_address = Mock(return_value=result)
        res = self.instance_service.allocate_elastic_address(ec2_client)
        self.assertTrue(ec2_client.allocate_address.called)
