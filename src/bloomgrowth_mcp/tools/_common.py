from .._json import error_envelope

NO_TOKEN = error_envelope(
    "not_configured", "No Bloom Growth access token. Send the X-BloomGrowth-Token header.", False
)
