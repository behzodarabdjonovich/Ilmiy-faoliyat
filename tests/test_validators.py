import pytest
from app.utils.validators import clean_text, safe_filename

def test_clean_text_optional_dash(): assert clean_text('-', required=False) is None
def test_clean_text_required_empty():
    with pytest.raises(ValueError): clean_text('   ')
def test_clean_text_limit():
    with pytest.raises(ValueError): clean_text('abcd', max_length=3)
def test_safe_filename(): assert safe_filename('../../xat № 1.pdf') == 'xat_1.pdf'
