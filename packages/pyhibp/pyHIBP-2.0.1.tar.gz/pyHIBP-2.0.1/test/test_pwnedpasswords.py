import hashlib
import time

import pytest

from pyHIBP import pwnedpasswords as pw


TEST_PASSWORD = "password"
TEST_PASSWORD_SHA1_HASH = hashlib.sha1(TEST_PASSWORD.encode('utf-8')).hexdigest()
# At least, I doubt someone would have used this (only directly specifying here for deterministic tests...)
TEST_PASSWORD_LIKELY_NOT_COMPROMISED = "&Q?t{%i|n+&qpyP/`/Lyr3<rK|N/M//;u^!fnR+j'lM)A+IGcgRGs[6mLY7yV-|x0bYB&L.JyaJ"
TEST_PASSWORD_LIKELY_NOT_COMPROMISED_HASH = hashlib.sha1(TEST_PASSWORD_LIKELY_NOT_COMPROMISED.encode('utf-8')).hexdigest()


@pytest.fixture(autouse=True)
def rate_limit():
    # There's no rate limit on passwords, but be nice anyway.
    time.sleep(1)


class TestIsPasswordBreached(object):
    def test_no_params_provided_raises(self):
        # is_password_breached(password=None, first_5_hash_chars=None, sha1_hash=None):
        with pytest.raises(AttributeError) as execinfo:
            pw.is_password_breached()
        assert "One of password, first_5_hash_chars, or sha1_hash must be provided." in str(execinfo.value)

    def test_password_not_string_raises(self):
        # is_password_breached(password=123, first_5_hash_chars=None, sha1_hash=None):
        with pytest.raises(AttributeError) as execinfo:
            pw.is_password_breached(password=123)
        assert "password must be a string type." in str(execinfo.value)

    def test_first_5_hash_chars_not_string_raises(self):
        # is_password_breached(password=None, first_5_hash_chars=123, sha1_hash=None):
        with pytest.raises(AttributeError) as execinfo:
            pw.is_password_breached(first_5_hash_chars=123)
        assert "first_5_hash_chars must be a string type." in str(execinfo.value)

    def test_first_5_hash_chars_not_length_five_raises(self):
        # is_password_breached(password=None, first_5_hash_chars="123456", sha1_hash=None):
        with pytest.raises(AttributeError) as execinfo:
            pw.is_password_breached(first_5_hash_chars="123456")
        assert "first_5_hash_chars must be of length 5." in str(execinfo.value)

    def test_sha1_hash_not_string_raises(self):
        # is_password_breached(password=None, first_5_hash_chars=None, sha1_hash=123):
        with pytest.raises(AttributeError) as execinfo:
            pw.is_password_breached(sha1_hash=123)
        assert "sha1_hash must be a string type." in str(execinfo.value)

    def test_list_of_partial_hashes_returned_with_5chars(self):
        # is_password_breached(password=None, first_5_hash_chars=TEST_PASSWORD_SHA1_HASH[0:5], sha1_hash=None):
        resp = pw.is_password_breached(first_5_hash_chars=TEST_PASSWORD_SHA1_HASH[0:5])
        assert isinstance(resp, list)
        assert len(resp) > 100
        match_found = False
        for entry in resp:
            if TEST_PASSWORD_SHA1_HASH[5:] in entry.lower():
                match_found = True
                break
        assert match_found

    def test_provide_password_to_function(self):
        resp = pw.is_password_breached(password="password")
        assert isinstance(resp, int)
        assert resp > 100

    def test_ensure_case_sensitivity_of_hash_does_not_matter(self):
        resp_one = pw.is_password_breached(sha1_hash=TEST_PASSWORD_SHA1_HASH.lower())
        assert isinstance(resp_one, int)
        assert resp_one > 100

        resp_two = pw.is_password_breached(sha1_hash=TEST_PASSWORD_SHA1_HASH.upper())
        assert isinstance(resp_two, int)
        assert resp_two > 100

        assert resp_one == resp_two

    def test_zero_count_result_for_non_breached_password(self):
        resp = pw.is_password_breached(password=TEST_PASSWORD_LIKELY_NOT_COMPROMISED)
        assert isinstance(resp, int)
        assert resp == 0
