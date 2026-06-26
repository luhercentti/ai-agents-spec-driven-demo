# Code Review

**Verdict:** request-changes

**Summary:** This diff enhances token verification and management while shifting to a token-based authentication approach. However, several issues related to security, error handling, and clarity need to be addressed.


## Findings

| Severity | File | Line | Issue | Suggestion |
|---|---|---|---|---|
| critical | server/auth.py | 6 | The APP_SECRET environment variable is not checked for None, which could lead to runtime errors or security vulnerabilities if the environment variable is absent. | Add a validation check to ensure APP_SECRET is not None and raise an appropriate exception if it is missing. |
| critical | server/auth.py | 35 | MD5 hashing is used for password storage, which is considered insecure and can be easily cracked. | Replace MD5 with a modern, secure password hashing algorithm like bcrypt, Argon2, or PBKDF2, and ensure the resulting hashed password is salted. |
| major | server/auth.py | 31 | The functionality for saving the new hashed password to the database is not implemented (marked by a TODO), leaving password resets effectively incomplete. | Implement the database logic for saving the hashed password securely. |
| major | server/auth.py | 20 | User data returned from verify_token is not validated to ensure it includes expected attributes, potentially causing downstream errors or vulnerabilities. | Validate the user object returned from get_user_by_token to confirm it has required fields such as 'id' and 'role'. |
| minor | server/auth.py | 17 | Accessing SECRET without verifying if it has been loaded properly may confuse future readers and lead to maintainability issues. | Log a warning or note in the code if SECRET is used without preliminary inspection to improve clarity. |
| minor | server/auth.py | 10 | The token extraction logic might fail if the authorization header value does not begin with 'Bearer '. | Check for 'Bearer ' prefix explicitly and return an appropriate error message if it's missing. |