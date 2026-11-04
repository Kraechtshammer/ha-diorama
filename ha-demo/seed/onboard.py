"""Goes through Home Assistant's onboarding on the first start, so the demo
opens straight on the dashboards with no setup.

Started in the background before Home Assistant on every start of the
container. It waits for Home Assistant to answer and does nothing when the
owner account already exists. Otherwise it creates the owner `demo` with
the password `demo` and finishes the remaining steps the way the
onboarding screens would. The trusted_networks login in configuration.yaml
then logs that user in without asking.
"""

import json
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "http://127.0.0.1:8123"
CLIENT_ID = "http://localhost:8124/"


def call(path, body=None, token=None, form=False):
    headers = {}
    data = None
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if body is not None:
        if form:
            data = urllib.parse.urlencode(body).encode()
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            data = json.dumps(body).encode()
            headers["Content-Type"] = "application/json"
    request = urllib.request.Request(BASE + path, data=data, headers=headers)
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.load(response)


for _ in range(300):
    try:
        steps = call("/api/onboarding")
        break
    except (urllib.error.URLError, ConnectionError, TimeoutError):
        time.sleep(2)
else:
    raise SystemExit("onboard.py: Home Assistant did not answer")

if any(step["step"] == "user" and step["done"] for step in steps):
    raise SystemExit(0)

code = call(
    "/api/onboarding/users",
    {"client_id": CLIENT_ID, "name": "Demo", "username": "demo", "password": "demo", "language": "en"},
)["auth_code"]
token = call(
    "/auth/token",
    {"grant_type": "authorization_code", "code": code, "client_id": CLIENT_ID},
    form=True,
)["access_token"]
call("/api/onboarding/core_config", {}, token)
call("/api/onboarding/analytics", {}, token)
call(
    "/api/onboarding/integration",
    {"client_id": CLIENT_ID, "redirect_uri": CLIENT_ID + "?auth_callback=1"},
    token,
)
print("onboard.py: created the user demo and finished onboarding")
