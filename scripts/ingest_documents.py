#!/usr/bin/env python3
"""Batch document ingestion script."""

import argparse
import asyncio
import os
import sys
import uuid

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings
from app.database.models import Base, Document, DocumentStatus, User
from app.services.ingestion_service import IngestionService
from app.services.auth_service import seed_default_users

settings = get_settings()


async def main(path: str):
    engine = create_async_engine(settings.database_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    Session = async_sessionmaker(engine, expire_on_commit=False)
    async with Session() as db:
        await seed_default_users(db)
        result = await db.execute(__import__("sqlalchemy").select(User).limit(1))
        user = result.scalar_one()

        for filename in os.listdir(path):
            filepath = os.path.join(path, filename)
            if not os.path.isfile(filepath):
                continue
            ext = os.path.splitext(filename)[1].lstrip(".").lower()
            doc = Document(
                id=uuid.uuid4(),
                title=filename,
                filename=filename,
                file_type=ext,
                status=DocumentStatus.PENDING,
                owner_id=user.id,
            )
            db.add(doc)
            await db.commit()
            await db.refresh(doc)

            service = IngestionService(db)
            await service.ingest_document(doc, filepath)
            print(f"Ingested: {filename} -> {doc.status.value}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True)
    args = parser.parse_args()
    asyncio.run(main(args.path))
