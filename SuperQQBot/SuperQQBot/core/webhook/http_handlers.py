from fastapi import Request, Response
from .models import ValidationRequest, ValidationResponse, serialize_response
from .crypto import generate_signature


async def handle_validation(request: Request, bot_secret: str):
    request_data = await request.json()
    validation_request = ValidationRequest(**request_data)

    # 假设secret_key是从bot_secret派生的，实际应用中应该更安全
    secret_key = bot_secret.encode()
    signature = generate_signature(validation_request.plain_token.encode(), secret_key)

    validation_response = ValidationResponse(
        plain_token=validation_request.plain_token,
        signature=signature.hex()
    )

    return Response(content=serialize_response(validation_response), media_type="application/json")
