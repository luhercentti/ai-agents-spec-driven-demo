# Code Review

**Verdict:** request-changes

**Summary:** The diff replaces a hardcoded secret and trivial token check with a more
realistic HMAC-based auth system, which is a meaningful improvement. However, there are
two critical issues — an unhandled `None` for `APP_SECRET` and the use of MD5 for
password hashing — that must be resolved before merging.

## Findings

| Severity | File | Line | Issue | Suggestion |
|---|---|---|---|---|
| critical | server/auth.py | 13 | `SECRET = os.environ.get("APP_SECRET")` — if the env var is not set, `SECRET` is `None`. The `hmac.new` call on line 30 will then raise `AttributeError: 'NoneType' object has no attribute 'encode'` at runtime. | Use `os.environ["APP_SECRET"]` (raises `KeyError` on startup if missing, which is explicit) or add a guard: `if not SECRET: raise RuntimeError("APP_SECRET is not set")` |
| critical | server/auth.py | 37 | `hashlib.md5` is used to hash passwords. MD5 is cryptographically broken and must never be used for passwords. | Use `bcrypt`, `argon2-cffi`, or `hashlib.pbkdf2_hmac` with a per-user salt. |
| major | server/auth.py | 30 | `hmac.new(...)` is not the correct call. The `hmac` module uses `hmac.new()` in Python 2; in Python 3 it is `hmac.new()` — this is actually valid, but the variable name `signature` shadows nothing and the token format `payload:signature` is never validated on the receiving end in `verify_token`. The token is looked up directly in the database without verifying the HMAC signature. | Either validate the HMAC in `verify_token` before the DB lookup, or document that tokens are opaque DB-issued tokens (and remove the HMAC generation entirely). |
| major | server/auth.py | 39 | `print(f"Password reset for user {user_id}: {hashed}")` logs the hashed password to stdout. Even a hashed value should not appear in logs. | Remove the print statement. Use a structured logger at DEBUG level if tracing is needed, and never log credential-related values. |
| minor | server/auth.py | 22 | `authorization.replace("Bearer ", "")` is fragile — it will silently pass through the full header value (including "Bearer ") if the prefix has different casing or extra whitespace. | Use `authorization.split(" ", 1)[-1]` or validate the prefix explicitly before stripping it. |
| info | server/auth.py | 43 | The `# TODO: save hashed to database` comment indicates `reset_password` is not yet functional. | Either implement it or raise `NotImplementedError` so callers know it does nothing. |
