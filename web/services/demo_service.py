import json
import urllib.request
import urllib.error

DEMO_ENDPOINT = "http://localhost:8000/demo/run"


def executar_demo(payload: dict) -> dict:
    """
    Chama o motor /demo/run sem depender de requests.
    Evita falha de import durante o load do WebApp.
    """
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        DEMO_ENDPOINT,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else ""
        raise RuntimeError(f"HTTPError {e.code} ao chamar /demo/run: {body}") from e
    except Exception as e:
        raise RuntimeError(f"Falha ao chamar /demo/run: {repr(e)}") from e
