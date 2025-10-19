# test_basics.py
def test_addition():
    """
    This test verifies that the testing environment is set up correctly.

    It ensures that:
    - Pytest is installed and can discover and run tests
    - A basic mathematical operation works as expected
    - The test suite reports a passing result for this trivial case

    Note:
    This is a standalone test and does not depend on any application code.
    It serves as an initial check to build confidence in the testing workflow.
    """
    assert 2 + 2 == 4