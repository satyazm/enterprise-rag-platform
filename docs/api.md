# API Reference

Base URL: `http://localhost:8000/api/v1`

## Auth

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register user |
| POST | `/auth/login` | Get JWT token |
| GET | `/auth/me` | Current user |

## Chat

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chat` | Send message, get cited answer |
| GET | `/chat/conversations` | List conversations |
| GET | `/chat/conversations/{id}/messages` | Get messages |

## Documents

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/documents` | List documents |
| POST | `/documents/upload` | Upload & ingest |
| DELETE | `/documents/{id}` | Delete (admin) |

## Admin

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/stats` | Dashboard stats |
| GET | `/admin/audit-logs` | Audit trail |
| POST | `/admin/evaluate` | Run evaluation |
