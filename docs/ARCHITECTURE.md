# Architecture Notes

## Processing pipeline

Upload/Import → validate → hash → extract → normalize → chunk → PostgreSQL → AI context → Gemini → chat history → React UI.

## Authorization boundary

Every document query is filtered by `user_id`. A valid JWT alone does not grant access to another user's document.

## Connector boundary

External providers are isolated behind `BaseConnector`; document processing receives bytes and metadata, so provider-specific code does not leak into core processing logic.
