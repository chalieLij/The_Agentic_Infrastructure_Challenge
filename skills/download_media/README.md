# Skill: Download Media

## Overview
Downloads a media file (video/image/audio) from a remote URL to local temporary storage.

## Input Schema (JSON)
```json
{
  "type": "object",
  "properties": {
    "url": {
      "type": "string",
      "format": "uri",
      "description": "The direct HTTP/HTTPS URL of the media asset."
    },
    "timeout_seconds": {
      "type": "integer",
      "default": 30,
      "description": "Maximum time to wait for download."
    }
  },
  "required": ["url"]
}
```

## Output Schema (JSON)
```json
{
  "type": "object",
  "properties": {
    "file_path": {
      "type": "string",
      "description": "Absolute local path to the downloaded file."
    },
    "file_hash": {
      "type": "string",
      "description": "SHA-256 hash of the content for verification."
    },
    "content_type": {
      "type": "string",
      "description": "MIME type of the downloaded file (e.g. video/mp4)."
    },
    "size_bytes": {
      "type": "integer",
      "description": "Size of the file in bytes."
    }
  },
  "required": ["file_path", "content_type"]
}
```
