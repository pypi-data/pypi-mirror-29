# Hash JupyterHub Authenticator

An authenticator for [JupyterHub](https://jupyterhub.readthedocs.io/en/latest/) where the password for each user is a secure hash of its username. Useful for environments where it's not suitable for users to authenticate with their Google/GitHub/etc. accounts.

## Installation

```bash
pip install jupyterhub-hashauthenticator
```

Should install it. It has no additional dependencies beyond JupyterHub and its dependencies.

You can then use this as your authenticator by adding the following lines to your `jupyterhub_config.py`:

```python
c.JupyterHub.authenticator_class = 'hashauthenticator.HashAuthenticator
c.HashAuthenticator.secret_key = 'my secret key'  # Defaults to ''
c.HashAuthenticator.password_length = 10          # Defaults to 6
c.HashAuthenticator.show_logins = True            # Optional, defaults to False
```

You can generate a good secret key with:
```bash
$ openssl rand -hex 32
0fafb0682a493485ed4e764d92abab1199d73246477c5daac7e0371ba541dd66
```

If the `show_logins` option is set to true, a CSV file containing login names and passwords will be served (to admins only) at `/hub/login_list`.

## Generating the password

This package comes with a command called `hashauthpw`. Example usage:

```bash
$ hashauthpw
usage: hashauthpw [-h] [--length LENGTH] username [secret_key]

$ hashauthpw pminkov my_key
939fd4
```
