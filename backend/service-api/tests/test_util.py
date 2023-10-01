from service.common.utils.utils import to_space_camel_case


def test_to_space_camel_case():
    assert to_space_camel_case('today') == 'Today'
