from .passwordhash import generate_password_digest
# To let the password script be run where JupyterHub isn't installed:
try:
  from .hashauthenticator import HashAuthenticator
except ImportError:
  print("Warning: Unable to import HashAuthenticator.\n"
        "Only generate_password_digest will be available.")
  HashAuthenticator = None


__all__ = ['HashAuthenticator', 'generate_password_digest']
