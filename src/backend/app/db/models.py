from __future__ import annotations

from datetime import UTC, datetime

from app.db.base import Base
from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


def utc_now() -> datetime:
    return datetime.now(UTC)


class JobSource(Base):
    __tablename__ = "job_sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    base_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    collection_method: Mapped[str | None] = mapped_column(String(100), nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    rate_limit: Mapped[str | None] = mapped_column(String(255), nullable=True)
    last_checked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )

    raw_snapshots: Mapped[list[RawJobSnapshot]] = relationship(
        back_populates="source", cascade="all, delete-orphan"
    )
    occurrences: Mapped[list[JobSourceOccurrence]] = relationship(
        back_populates="source", cascade="all, delete-orphan"
    )


class RawJobSnapshot(Base):
    __tablename__ = "raw_job_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("job_sources.id"), nullable=False)
    external_job_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    raw_html: Mapped[str | None] = mapped_column(Text, nullable=True)
    content_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    collected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )

    source: Mapped[JobSource] = relationship(back_populates="raw_snapshots")


class JobOffer(Base):
    __tablename__ = "job_offers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    company_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    company_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    normalized_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    job_type: Mapped[str | None] = mapped_column(String(120), nullable=True)
    contract_type: Mapped[str | None] = mapped_column(String(120), nullable=True)
    location_text: Mapped[str | None] = mapped_column(String(255), nullable=True)
    city: Mapped[str | None] = mapped_column(String(120), nullable=True)
    region: Mapped[str | None] = mapped_column(String(120), nullable=True)
    country: Mapped[str | None] = mapped_column(String(120), nullable=True)
    remote_type: Mapped[str | None] = mapped_column(String(80), nullable=True)
    salary_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_currency: Mapped[str | None] = mapped_column(String(20), nullable=True)
    salary_period: Mapped[str | None] = mapped_column(String(40), nullable=True)
    duration: Mapped[str | None] = mapped_column(String(120), nullable=True)
    experience_level: Mapped[str | None] = mapped_column(String(120), nullable=True)
    education_level: Mapped[str | None] = mapped_column(String(120), nullable=True)
    industry: Mapped[str | None] = mapped_column(String(120), nullable=True)
    job_category: Mapped[str | None] = mapped_column(String(120), nullable=True)
    publication_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    expiration_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    first_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )
    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )
    status: Mapped[str] = mapped_column(String(80), nullable=False, default="active")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )

    occurrences: Mapped[list[JobSourceOccurrence]] = relationship(
        back_populates="job_offer", cascade="all, delete-orphan"
    )


class JobSourceOccurrence(Base):
    __tablename__ = "job_source_occurrences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_offer_id: Mapped[int] = mapped_column(ForeignKey("job_offers.id"), nullable=False)
    source_id: Mapped[int] = mapped_column(ForeignKey("job_sources.id"), nullable=False)
    external_job_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    collected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_primary: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    status: Mapped[str] = mapped_column(String(80), nullable=False, default="active")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )

    job_offer: Mapped[JobOffer] = relationship(back_populates="occurrences")
    source: Mapped[JobSource] = relationship(back_populates="occurrences")

    __table_args__ = (
        UniqueConstraint(
            "job_offer_id",
            "source_id",
            "external_job_id",
            name="uq_job_occurrence_offer_source_external",
        ),
    )


class UserProfile(Base):
    """Mono-user profile used as the reference for later matching."""

    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    mobility: Mapped[str | None] = mapped_column(String(100), nullable=True)
    remote_preference: Mapped[str | None] = mapped_column(String(50), nullable=True)
    desired_salary_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    desired_salary_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    availability_date: Mapped[str | None] = mapped_column(String(50), nullable=True)
    internship_duration_weeks: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )

    contract_types: Mapped[list[PreferredContractType]] = relationship(
        back_populates="profile", cascade="all, delete-orphan"
    )
    job_types: Mapped[list[PreferredJobType]] = relationship(
        back_populates="profile", cascade="all, delete-orphan"
    )
    job_roles: Mapped[list[PreferredJobRole]] = relationship(
        back_populates="profile", cascade="all, delete-orphan"
    )
    industries: Mapped[list[PreferredIndustry]] = relationship(
        back_populates="profile", cascade="all, delete-orphan"
    )
    skills: Mapped[list[UserSkill]] = relationship(
        back_populates="profile", cascade="all, delete-orphan"
    )
    technologies: Mapped[list[UserTechnology]] = relationship(
        back_populates="profile", cascade="all, delete-orphan"
    )
    languages: Mapped[list[UserLanguage]] = relationship(
        back_populates="profile", cascade="all, delete-orphan"
    )
    preferred_companies: Mapped[list[PreferredCompany]] = relationship(
        back_populates="profile", cascade="all, delete-orphan"
    )


class PreferredContractType(Base):
    __tablename__ = "preferred_contract_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.id"), nullable=False)
    contract_type: Mapped[str] = mapped_column(String(100), nullable=False)
    preference_level: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )

    profile: Mapped[UserProfile] = relationship(back_populates="contract_types")

    __table_args__ = (
        UniqueConstraint(
            "profile_id",
            "contract_type",
            name="uq_preferred_contract_type_profile_and_value",
        ),
    )


class PreferredJobType(Base):
    __tablename__ = "preferred_job_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.id"), nullable=False)
    job_type: Mapped[str] = mapped_column(String(100), nullable=False)
    preference_level: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )

    profile: Mapped[UserProfile] = relationship(back_populates="job_types")

    __table_args__ = (
        UniqueConstraint("profile_id", "job_type", name="uq_preferred_job_type_profile_and_value"),
    )


class PreferredJobRole(Base):
    __tablename__ = "preferred_job_roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.id"), nullable=False)
    job_role: Mapped[str] = mapped_column(String(255), nullable=False)
    preference_level: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )

    profile: Mapped[UserProfile] = relationship(back_populates="job_roles")

    __table_args__ = (
        UniqueConstraint("profile_id", "job_role", name="uq_preferred_job_role_profile_and_value"),
    )


class PreferredIndustry(Base):
    __tablename__ = "preferred_industries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.id"), nullable=False)
    industry: Mapped[str] = mapped_column(String(255), nullable=False)
    preference_level: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )

    profile: Mapped[UserProfile] = relationship(back_populates="industries")

    __table_args__ = (
        UniqueConstraint("profile_id", "industry", name="uq_preferred_industry_profile_and_value"),
    )


class UserSkill(Base):
    __tablename__ = "user_skills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.id"), nullable=False)
    skill_name: Mapped[str] = mapped_column(String(255), nullable=False)
    proficiency_level: Mapped[str | None] = mapped_column(String(50), nullable=True)
    years_experience: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )

    profile: Mapped[UserProfile] = relationship(back_populates="skills")

    __table_args__ = (
        UniqueConstraint("profile_id", "skill_name", name="uq_user_skill_profile_and_name"),
    )


class UserTechnology(Base):
    __tablename__ = "user_technologies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.id"), nullable=False)
    technology_name: Mapped[str] = mapped_column(String(255), nullable=False)
    proficiency_level: Mapped[str | None] = mapped_column(String(50), nullable=True)
    years_experience: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )

    profile: Mapped[UserProfile] = relationship(back_populates="technologies")

    __table_args__ = (
        UniqueConstraint(
            "profile_id",
            "technology_name",
            name="uq_user_technology_profile_and_name",
        ),
    )


class UserLanguage(Base):
    __tablename__ = "user_languages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.id"), nullable=False)
    language_name: Mapped[str] = mapped_column(String(100), nullable=False)
    proficiency_level: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )

    profile: Mapped[UserProfile] = relationship(back_populates="languages")

    __table_args__ = (
        UniqueConstraint("profile_id", "language_name", name="uq_user_language_profile_and_name"),
    )


class PreferredCompany(Base):
    __tablename__ = "preferred_companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.id"), nullable=False)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    preference_level: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )

    profile: Mapped[UserProfile] = relationship(back_populates="preferred_companies")

    __table_args__ = (
        UniqueConstraint(
            "profile_id",
            "company_name",
            name="uq_preferred_company_profile_and_name",
        ),
    )
