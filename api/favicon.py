def handler(request):
    # Return 204 No Content for favicon.ico requests
    return (b"", 204, {"Content-Type": "image/x-icon"})