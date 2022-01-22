import bigjsonprocessor.processor as p
import pytest

def test_calulateBMI():
	pytest.raises(ZeroDivisionError, p.compute_BMI, 0,10)
