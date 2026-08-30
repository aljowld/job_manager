"""drop raw_job_snapshot unique constraint on source_id/external_job_id

Revision ID: 20260830_000001
Revises: 20240829_000001
Create Date: 2026-08-30 00:00:00.000000

"""

from __future__ import annotations

from alembic import op

# revision identifiers, used by Alembic.
revision = "20260830_000001"
down_revision = "20240829_000001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Raw snapshots must accumulate history across recollections of the same
    # external job; only JobSourceOccurrence enforces per-offer uniqueness.
    op.drop_constraint(
        "uq_raw_job_snapshot_source_external_id", "raw_job_snapshots", type_="unique"
    )


def downgrade() -> None:
    op.create_unique_constraint(
        "uq_raw_job_snapshot_source_external_id",
        "raw_job_snapshots",
        ["source_id", "external_job_id"],
    )
