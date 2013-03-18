from cyder.cydns.forms import DNSForm
from django import forms
from cyder.cydns.address_record.models import AddressRecord


class AddressRecordForm(DNSForm):
    class Meta:
        model = AddressRecord
        exclude = ('ip_upper', 'ip_lower', 'reverse_domain', 'fqdn')
        fields = ('label', 'domain', 'ip_type', 'ip_str', 'views', 'ttl',
                  'description')
        widgets = {'views': forms.CheckboxSelectMultiple}


class AddressRecordFQDNForm(AddressRecordForm):
    class Meta:
        model = AddressRecord
        fields = ('fqdn', 'ip_type', 'ip_str', 'views', 'ttl', 'description')
        widgets = {'views': forms.CheckboxSelectMultiple}
