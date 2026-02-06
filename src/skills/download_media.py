def download(input_data: dict) -> dict:
    """
    Mock implementation of download media.
    Expected input_data: {"url": "...", "timeout_seconds": ...}
    """
    if not isinstance(input_data, dict):
        raise TypeError("Input must be a dictionary")
    
    if "url" not in input_data:
        raise TypeError("Missing required field 'url'")

    return {
        "file_path": "/tmp/mock_download.mp4",
        "file_hash": "mock_hash_123",
        "content_type": "video/mp4",
        "size_bytes": 1024
    }
