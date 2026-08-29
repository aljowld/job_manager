"""User profile routes."""

from __future__ import annotations

from collections.abc import Iterable

from fastapi import APIRouter, Depends
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core.exceptions import ProfileNotFoundError
from app.db.models import (
    PreferredCompany,
    PreferredContractType,
    PreferredIndustry,
    PreferredJobRole,
    PreferredJobType,
    UserLanguage,
    UserProfile,
    UserSkill,
    UserTechnology,
)
from app.schemas.profile import ProfileInputSchema, ProfileOutputSchema

router = APIRouter(tags=["profile"])


def _deduplicate_by_key(items: Iterable[object], key_name: str) -> list[object]:
    """Keep only the first instance of each value while preserving input order."""
    seen: set[str] = set()
    result: list[object] = []
    for item in items:
        key = getattr(item, key_name, None)
        if key is None:
            continue
        normalized = str(key).strip().lower()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        result.append(item)
    return result


def _serialize_profile(profile: UserProfile) -> ProfileOutputSchema:
    """Serialize SQLAlchemy profile model to a response schema."""
    contract_types = list(profile.contract_types)
    job_types = list(profile.job_types)
    job_roles = list(profile.job_roles)
    industries = list(profile.industries)
    skills = list(profile.skills)
    technologies = list(profile.technologies)
    languages = list(profile.languages)
    preferred_companies = list(profile.preferred_companies)

    return ProfileOutputSchema(
        id=profile.id,
        full_name=profile.full_name,
        email=profile.email,
        phone=profile.phone,
        location=profile.location,
        mobility=profile.mobility,
        remote_preference=profile.remote_preference,
        desired_salary_min=profile.desired_salary_min,
        desired_salary_max=profile.desired_salary_max,
        availability_date=profile.availability_date,
        internship_duration_weeks=profile.internship_duration_weeks,
        contract_types=[
            {"contract_type": item.contract_type, "preference_level": item.preference_level}
            for item in contract_types
        ],
        job_types=[
            {"job_type": item.job_type, "preference_level": item.preference_level}
            for item in job_types
        ],
        job_roles=[
            {"job_role": item.job_role, "preference_level": item.preference_level}
            for item in job_roles
        ],
        industries=[
            {"industry": item.industry, "preference_level": item.preference_level}
            for item in industries
        ],
        skills=[
            {
                "skill_name": item.skill_name,
                "proficiency_level": item.proficiency_level,
                "years_experience": item.years_experience,
            }
            for item in skills
        ],
        technologies=[
            {
                "technology_name": item.technology_name,
                "proficiency_level": item.proficiency_level,
                "years_experience": item.years_experience,
            }
            for item in technologies
        ],
        languages=[
            {"language_name": item.language_name, "proficiency_level": item.proficiency_level}
            for item in languages
        ],
        preferred_companies=[
            {"company_name": item.company_name, "preference_level": item.preference_level}
            for item in preferred_companies
        ],
    )


def _replace_profile_collections(profile: UserProfile, payload: ProfileInputSchema) -> None:
    """Replace the profile's nested collections with a canonical, deduplicated set."""
    profile.full_name = payload.full_name
    profile.email = payload.email
    profile.phone = payload.phone
    profile.location = payload.location
    profile.mobility = payload.mobility
    profile.remote_preference = payload.remote_preference
    profile.desired_salary_min = payload.desired_salary_min
    profile.desired_salary_max = payload.desired_salary_max
    profile.availability_date = payload.availability_date
    profile.internship_duration_weeks = payload.internship_duration_weeks

    db = Session.object_session(profile)
    if db is not None:
        db.execute(
            delete(PreferredContractType).where(PreferredContractType.profile_id == profile.id)
        )
        db.execute(delete(PreferredJobType).where(PreferredJobType.profile_id == profile.id))
        db.execute(delete(PreferredJobRole).where(PreferredJobRole.profile_id == profile.id))
        db.execute(delete(PreferredIndustry).where(PreferredIndustry.profile_id == profile.id))
        db.execute(delete(UserSkill).where(UserSkill.profile_id == profile.id))
        db.execute(delete(UserTechnology).where(UserTechnology.profile_id == profile.id))
        db.execute(delete(UserLanguage).where(UserLanguage.profile_id == profile.id))
        db.execute(delete(PreferredCompany).where(PreferredCompany.profile_id == profile.id))

    for item in _deduplicate_by_key(payload.contract_types, "contract_type"):
        profile.contract_types.append(
            PreferredContractType(
                contract_type=item.contract_type,
                preference_level=item.preference_level.value,
            )
        )
    for item in _deduplicate_by_key(payload.job_types, "job_type"):
        profile.job_types.append(
            PreferredJobType(
                job_type=item.job_type,
                preference_level=item.preference_level.value,
            )
        )
    for item in _deduplicate_by_key(payload.job_roles, "job_role"):
        profile.job_roles.append(
            PreferredJobRole(
                job_role=item.job_role,
                preference_level=item.preference_level.value,
            )
        )
    for item in _deduplicate_by_key(payload.industries, "industry"):
        profile.industries.append(
            PreferredIndustry(
                industry=item.industry,
                preference_level=item.preference_level.value,
            )
        )
    for item in _deduplicate_by_key(payload.skills, "skill_name"):
        profile.skills.append(
            UserSkill(
                skill_name=item.skill_name,
                proficiency_level=item.proficiency_level,
                years_experience=item.years_experience,
            )
        )
    for item in _deduplicate_by_key(payload.technologies, "technology_name"):
        profile.technologies.append(
            UserTechnology(
                technology_name=item.technology_name,
                proficiency_level=item.proficiency_level,
                years_experience=item.years_experience,
            )
        )
    for item in _deduplicate_by_key(payload.languages, "language_name"):
        profile.languages.append(
            UserLanguage(
                language_name=item.language_name,
                proficiency_level=item.proficiency_level,
            )
        )
    for item in _deduplicate_by_key(payload.preferred_companies, "company_name"):
        profile.preferred_companies.append(
            PreferredCompany(
                company_name=item.company_name,
                preference_level=item.preference_level.value,
            )
        )


@router.get("/profile", response_model=ProfileOutputSchema)
def get_profile(db: Session = Depends(get_db)) -> ProfileOutputSchema:
    """Return the single persisted profile, or raise 404 if none exists yet."""
    profile = db.execute(select(UserProfile)).scalar_one_or_none()
    if profile is None:
        raise ProfileNotFoundError("User profile has not been created yet")
    return _serialize_profile(profile)


@router.put("/profile", response_model=ProfileOutputSchema)
def put_profile(
    payload: ProfileInputSchema,
    db: Session = Depends(get_db),
) -> ProfileOutputSchema:
    """Create or replace the singleton user profile in a transactional way."""
    try:
        profile = db.execute(select(UserProfile)).scalar_one_or_none()
        if profile is None:
            profile = UserProfile()
            db.add(profile)
            db.flush()

        _replace_profile_collections(profile, payload)
        db.commit()
        db.refresh(profile)
        return _serialize_profile(profile)
    except Exception:
        db.rollback()
        raise
