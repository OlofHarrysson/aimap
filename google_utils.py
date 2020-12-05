from pathlib import Path


def read_api_key():
  api_path = Path("keys.txt")
  assert api_path.exists(), f"API-key file doesn't exist at {api_path}"
  with open(api_path) as f:
    key = f.read()
  return key
