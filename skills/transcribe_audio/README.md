# Skill: Transcribe Audio

## Overview
Extracts audio from a video file (if necessary) and generates a textual transcript with timestamps.

## Input Schema (JSON)
```json
{
  "type": "object",
  "properties": {
    "file_path": {
      "type": "string",
      "description": "Local path to the video or audio file."
    },
    "language_hint": {
      "type": "string",
      "description": "Optional ISO code (e.g., 'en', 'es') to guide the model."
    }
  },
  "required": ["file_path"]
}
```

## Output Schema (JSON)
```json
{
  "type": "object",
  "properties": {
    "full_text": {
      "type": "string",
      "description": "Complete transcript text."
    },
    "segments": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "start": { "type": "number", "description": "Start time in seconds" },
          "end": { "type": "number", "description": "End time in seconds" },
          "text": { "type": "string", "description": "Transcribed text for this segment" },
          "confidence": { "type": "number", "description": "0.0 to 1.0 confidence score" }
        }
      }
    },
    "detected_language": {
      "type": "string",
      "description": "ISO code of the detected language."
    }
  },
  "required": ["full_text", "segments"]
}
```
