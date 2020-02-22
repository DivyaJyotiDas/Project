from mock import MagicMock
import pytest
import mock

class ProductionClass:
    def method(self):
        pass

class EmailParts:
    subject=None
    html_part=None
    text_part=None
    to_email=None
    _from_email=None
    request=None
    locale=None
    attachments=None

    @property
    def from_email(self):
        return self._from_email or 'divyajyotidas15@gmail.com'

    @from_email.setter
    def from_email(self, value):
        self._from_email = value

@mock.patch('api.tests.ProductionClass.method')
def test_prod_class(mock_val):
    mock_val.return_value='Ford'
    mock_val.assert_called()

def test_from_email():
    ep = EmailParts()
    ep.from_email='roshni@gmail.com'
    print(ep.from_email)
    ep = MagicMock()
    ep._from_email.return_value='divya@gmail.com'
    assert ep.from_email == ep._from_email


