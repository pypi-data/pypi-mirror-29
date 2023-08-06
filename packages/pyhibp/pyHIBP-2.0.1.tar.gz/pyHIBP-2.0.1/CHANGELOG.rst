v2.0.1 (2018-03-09)
-------------------
- **Deprecation warning**: The function ``is_password_breached`` has moved from ``pyHIBP`` to the module named ``pwnedpasswords``. A wrapper has
  been left to ease transition to the new function; access via ``from pyHIBP import pwnedpasswords``.
- The Pwned Passwords API version 2 has been released, and as such the following changes were made:
- ``is_password_breached`` no longer transmits the full SHA-1 hash to the Pwned Passwords API endpoint. This means any
  password that we want to check--such as a user's signup password--is secure. This is accomplished by transmitting
  the first 5 characters of the SHA-1 hash, and parsing the resultant list of partial SHA hashes for a match to the
  supplied password, or SHA-1 hash.
- The behavior of the prior ``is_password_breached()`` as implemented in v2.0.0 which submitted the full SHA-1 hash
  was dropped for added security.
- In addition to ``password`` and ``sha1_hash``, ``pwnedpasswords.is_password_breached()`` now accepts ``first_5_hash_chars``.
  This is to be set to the first five characters of a SHA-1 hash, and will return a list of partial hashes, along with
  the number of times the hash value in question was found in the Pwned Passwords corpus. This could be useful if you
  wish to perform verification of the hashes in the application importing this module.
- If ``password`` or ``sha1_hash`` is provided, the return value will now be an integer, corresponding to the number
  of times that password was located in the Pwned Passwords corpus, as per above. Integer zero (0) is returned if there
  was no match located, so one can still execute a call in the manner of ``if pw.is_password_breached():``.
- Unrelated to the code changes, the Pwned Passwords API (i.e, ``is_password_breached``) is no longer rate-limited.
  For more information, please see Troy Hunt's `post announcing Pwned Passwords v2 <https://www.troyhunt.com/ive-just-launched-pwned-passwords-version-2/>`_


v2.0.0 (2018-02-01)
-------------------
- Initial release.
