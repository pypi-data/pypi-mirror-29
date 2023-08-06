from unittest import TestCase

from mock import Mock

from cloudshell.cp.aws.domain.services.ec2.subnet import SubnetService


class TestSubnetService(TestCase):
    def setUp(self):

        self.vpc = Mock()
        self.cidr = '10.0.0.0/24'
        self.vpc_name = 'name'
        self.reservation_id = 'res'
        self.tag_srv = Mock()
        self.subnet_waiter = Mock()
        self.subnet_srv = SubnetService(self.tag_srv, self.subnet_waiter)

    def test_create_subnet_for_vpc(self):
        subnet = Mock()
        self.vpc.create_subnet = Mock(return_value=subnet)
        self.subnet_srv._get_subnet_name=Mock(return_value=self.vpc_name)

        self.subnet_srv.create_subnet_for_vpc(self.vpc, self.cidr, self.vpc_name, self.reservation_id)

        self.vpc.create_subnet.assert_called_with(CidrBlock=self.cidr)
        self.subnet_waiter.wait.assert_called_with(subnet, self.subnet_waiter.AVAILABLE)
        self.tag_srv.get_default_tags.assert_called_with(self.vpc_name, self.reservation_id)
        self.assertEqual(subnet, self.vpc.create_subnet())

    def test_get_subnet_from_vpc(self):
        vpc = Mock()
        vpc.subnets = Mock()
        vpc.subnets.all = Mock(return_value=[1])
        subnet = self.subnet_srv.get_subnet_from_vpc(vpc)
        self.assertEqual(1, subnet)

    def test_get_subnet_from_vpc_fault(self):
        vpc = Mock()
        vpc.subnets = Mock()
        vpc.subnets.all = Mock(return_value=[])
        self.assertRaises(ValueError, self.subnet_srv.get_subnet_from_vpc, vpc)

    def test_delete_subnet(self):
        subnet = Mock()
        res = self.subnet_srv.detele_subnet(subnet)
        self.assertTrue(res)
        self.assertTrue(subnet.delete.called)

    def test_get_subnet_name(self):
        subnet_name = self.subnet_srv._get_subnet_name('some_subnet')
        self.assertEquals(subnet_name, 'VPC Name: some_subnet')
