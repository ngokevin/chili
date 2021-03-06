from django.test import TestCase
from django.core.exceptions import ValidationError

from cyder.cydhcp.site.models import Site
from cyder.cydhcp.network.models import Network
from cyder.cydhcp.range.models import Range
from cyder.cydns.domain.models import Domain
from cyder.cydns.ip.models import ipv6_to_longs


class NetworkTests(TestCase):

    def do_basic_add(self, network, prefixlen, ip_type,
                     ame=None, number=None, site=None):
        s = Network(network_str=network + "/" + prefixlen,
                    ip_type=ip_type, site=site)
        s.clean()
        s.save()
        self.assertTrue(s)
        return s

    def do_basic_add_site(self, name, parent=None):
        s = Site(name=name, parent=parent)
        s.clean()
        s.save()
        self.assertTrue(s)
        return s

    def test1_create_ipv6(self):
        network = "f::"
        prefixlen = "24"
        kwargs = {'network': network,
                  'prefixlen': prefixlen,
                  'ip_type': '6'}
        s = self.do_basic_add(**kwargs)
        str(s)
        s.__repr__()
        self.assertTrue(s)

    def test2_create_ipv6(self):
        network = "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff"
        prefixlen = "24"
        kwargs = {'network': network,
                  'prefixlen': prefixlen,
                  'ip_type': '6'}
        s = self.do_basic_add(**kwargs)
        str(s)
        s.__repr__()
        self.assertTrue(s)
        ip_upper, ip_lower = ipv6_to_longs(network)
        self.assertEqual(s.ip_upper, ip_upper)
        self.assertEqual(s.ip_lower, ip_lower)

    def test_bad_resize(self):
        network = "129.0.0.0"
        prefixlen = "24"
        kwargs = {'network': network,
                  'prefixlen': prefixlen,
                  'ip_type': '4'}
        s = self.do_basic_add(**kwargs)
        self.assertTrue(s)

        d = Domain(name="asdf")
        d.save()

        start_str = "129.0.0.1"
        end_str = "129.0.0.255"
        network = s

        r = Range(start_str=start_str, end_str=end_str, network=network,
                ip_type='4')
        r.save()

        self.assertEqual(r.network, s)
        self.assertTrue(len(s.range_set.all()) == 1)

        s.network_str = "129.0.0.0/25"
        self.assertRaises(ValidationError, s.clean)

    def test_bad_delete(self):
        network = "129.0.0.0"
        prefixlen = "24"
        kwargs = {'network': network,
                  'prefixlen': prefixlen,
                  'ip_type': '4'}
        s = self.do_basic_add(**kwargs)
        s_pk = s.pk
        self.assertTrue(s)

        d = Domain(name="asdf")
        d.save()

        start_str = "129.0.0.1"
        end_str = "129.0.0.255"
        network = s

        r = Range(start_str=start_str, end_str=end_str, network=network,
                ip_type='4')
        r.clean()
        r.save()

        self.assertEqual(r.network, s)
        self.assertTrue(len(s.range_set.all()) == 1)

        self.assertRaises(ValidationError, s.delete)
        self.assertTrue(Network.objects.get(pk=s_pk))

        r.delete()
        s.delete()
        self.assertEqual(len(Network.objects.filter(pk=s_pk)), 0)

    def test_get_related_networks(self):
        network = "129.0.0.1"
        prefixlen = "20"
        kwargs = {'network': network,
                  'prefixlen': prefixlen,
                  'ip_type': '4'}
        s1 = self.do_basic_add(**kwargs)

        network = "129.0.2.1"
        prefixlen = "25"
        kwargs = {'network': network,
                  'prefixlen': prefixlen,
                  'ip_type': '4'}
        s2 = self.do_basic_add(**kwargs)

        network = "129.0.4.1"
        prefixlen = "29"
        kwargs = {'network': network,
                  'prefixlen': prefixlen,
                  'ip_type': '4'}
        s3 = self.do_basic_add(**kwargs)

        network = "129.0.2.1"
        prefixlen = "29"
        kwargs = {'network': network,
                  'prefixlen': prefixlen,
                  'ip_type': '4'}
        s4 = self.do_basic_add(**kwargs)

        related = s1.get_related_networks()
        self.assertEqual(set([s1, s2, s3, s4]), set(related))

    def test_get_related_sites(self):
        s1 = self.do_basic_add_site("Kerr")
        s2 = self.do_basic_add_site("Business", parent=s1)
        s3 = self.do_basic_add_site("Registration", parent=s1)

        network = "129.0.0.0"
        prefixlen = "19"
        kwargs = {'network': network,
                  'prefixlen': prefixlen,
                  'ip_type': '4',
                  'site': s1}
        n1 = self.do_basic_add(**kwargs)

        network = "129.0.1.0"
        prefixlen = "24"
        kwargs = {'network': network,
                  'prefixlen': prefixlen,
                  'ip_type': '4',
                  'site': s2}
        n2 = self.do_basic_add(**kwargs)

        network = "129.0.1.0"
        prefixlen = "22"
        kwargs = {'network': network,
                  'prefixlen': prefixlen,
                  'ip_type': '4',
                  'site': s3}
        n3 = self.do_basic_add(**kwargs)

        network = "129.0.1.0"
        prefixlen = "25"
        kwargs = {'network': network,
                  'prefixlen': prefixlen,
                  'ip_type': '4'}
        n4 = self.do_basic_add(**kwargs)

        networks_related = n1.get_related_networks()
        self.assertEqual(networks_related, set([n1, n2, n3, n4]))
        """            a
        if we choose s1 as a site then s2, s3, n1, n2, n3, and n4 are returned

        if we choose n2 then n3 and n4 should be returned

        if we choose s3 then n2, n3, and n4 s

        if we choose
        """
