"""initial persistence schema

Revision ID: 20240829_000001
Revises: 
Create Date: 2024-08-29 00:00:00.000000

"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "20240829_000001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "job_sources",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("base_url", sa.String(length=500), nullable=True),
        sa.Column("collection_method", sa.String(length=100), nullable=True),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.Column("rate_limit", sa.String(length=255), nullable=True),
        sa.Column("last_checked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", name="uq_job_sources_name"),
    )

    op.create_table(
        "raw_job_snapshots",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("source_id", sa.Integer(), nullable=False),
        sa.Column("external_job_id", sa.String(length=255), nullable=True),
        sa.Column("source_url", sa.String(length=500), nullable=True),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("raw_html", sa.Text(), nullable=True),
        sa.Column("content_hash", sa.String(length=128), nullable=True),
        sa.Column("collected_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["source_id"], ["job_sources.id"], name="fk_raw_job_snapshots_source_id_job_sources"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("source_id", "external_job_id", name="uq_raw_job_snapshot_source_external_id"),
    )

    op.create_table(
        "job_offers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("company_name", sa.String(length=255), nullable=True),
        sa.Column("company_description", sa.Text(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("normalized_description", sa.Text(), nullable=True),
        sa.Column("job_type", sa.String(length=120), nullable=True),
        sa.Column("contract_type", sa.String(length=120), nullable=True),
        sa.Column("location_text", sa.String(length=255), nullable=True),
        sa.Column("city", sa.String(length=120), nullable=True),
        sa.Column("region", sa.String(length=120), nullable=True),
        sa.Column("country", sa.String(length=120), nullable=True),
        sa.Column("remote_type", sa.String(length=80), nullable=True),
        sa.Column("salary_min", sa.Integer(), nullable=True),
        sa.Column("salary_max", sa.Integer(), nullable=True),
        sa.Column("salary_currency", sa.String(length=20), nullable=True),
        sa.Column("salary_period", sa.String(length=40), nullable=True),
        sa.Column("duration", sa.String(length=120), nullable=True),
        sa.Column("experience_level", sa.String(length=120), nullable=True),
        sa.Column("education_level", sa.String(length=120), nullable=True),
        sa.Column("industry", sa.String(length=120), nullable=True),
        sa.Column("job_category", sa.String(length=120), nullable=True),
        sa.Column("publication_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expiration_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("first_seen_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=80), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "job_source_occurrences",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("job_offer_id", sa.Integer(), nullable=False),
        sa.Column("source_id", sa.Integer(), nullable=False),
        sa.Column("external_job_id", sa.String(length=255), nullable=True),
        sa.Column("source_url", sa.String(length=500), nullable=True),
        sa.Column("collected_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_primary", sa.Boolean(), nullable=False),
        sa.Column("status", sa.String(length=80), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["job_offer_id"], ["job_offers.id"], name="fk_job_source_occurrences_job_offer_id_job_offers"),
        sa.ForeignKeyConstraint(["source_id"], ["job_sources.id"], name="fk_job_source_occurrences_source_id_job_sources"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("job_offer_id", "source_id", "external_job_id", name="uq_job_occurrence_offer_source_external"),
    )


def downgrade() -> None:
    op.drop_table("job_source_occurrences")
    op.drop_table("raw_job_snapshots")
    op.drop_table("job_offers")
    op.drop_table("job_sources")
