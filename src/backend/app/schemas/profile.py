"""Pydantic schemas for user profile and preferences."""

from enum import StrEnum

from pydantic import BaseModel, Field


class PreferenceLevelEnum(StrEnum):
    """Preference level for matching and filtering."""

    REQUIRED = "REQUIRED"
    VERY_IMPORTANT = "VERY_IMPORTANT"
    IMPORTANT = "IMPORTANT"
    BONUS = "BONUS"
    AVOID = "AVOID"
    EXCLUDED = "EXCLUDED"


class PreferredContractTypeSchema(BaseModel):
    """Preferred contract type."""

    contract_type: str = Field(..., min_length=1, max_length=100)
    preference_level: PreferenceLevelEnum

    model_config = {"from_attributes": True}


class PreferredJobTypeSchema(BaseModel):
    """Preferred job type."""

    job_type: str = Field(..., min_length=1, max_length=100)
    preference_level: PreferenceLevelEnum

    model_config = {"from_attributes": True}


class PreferredJobRoleSchema(BaseModel):
    """Preferred job role."""

    job_role: str = Field(..., min_length=1, max_length=255)
    preference_level: PreferenceLevelEnum

    model_config = {"from_attributes": True}


class PreferredIndustrySchema(BaseModel):
    """Preferred industry."""

    industry: str = Field(..., min_length=1, max_length=255)
    preference_level: PreferenceLevelEnum

    model_config = {"from_attributes": True}


class UserSkillSchema(BaseModel):
    """User skill."""

    skill_name: str = Field(..., min_length=1, max_length=255)
    proficiency_level: str | None = Field(None, max_length=50)
    years_experience: int | None = Field(None, ge=0)

    model_config = {"from_attributes": True}


class UserTechnologySchema(BaseModel):
    """User technology."""

    technology_name: str = Field(..., min_length=1, max_length=255)
    proficiency_level: str | None = Field(None, max_length=50)
    years_experience: int | None = Field(None, ge=0)

    model_config = {"from_attributes": True}


class UserLanguageSchema(BaseModel):
    """User language."""

    language_name: str = Field(..., min_length=1, max_length=100)
    proficiency_level: str = Field(..., min_length=1, max_length=50)

    model_config = {"from_attributes": True}


class PreferredCompanySchema(BaseModel):
    """Preferred or excluded company."""

    company_name: str = Field(..., min_length=1, max_length=255)
    preference_level: PreferenceLevelEnum

    model_config = {"from_attributes": True}


class ProfileInputSchema(BaseModel):
    """Input schema for creating or replacing a single-user profile."""

    full_name: str | None = Field(None, max_length=255)
    email: str | None = Field(None, max_length=255)
    phone: str | None = Field(None, max_length=20)
    location: str | None = Field(None, max_length=255)
    mobility: str | None = Field(None, max_length=100)
    remote_preference: str | None = Field(None, max_length=50)
    desired_salary_min: int | None = Field(None, ge=0)
    desired_salary_max: int | None = Field(None, ge=0)
    availability_date: str | None = Field(None, max_length=50)
    internship_duration_weeks: int | None = Field(None, ge=0)
    contract_types: list[PreferredContractTypeSchema] = Field(default_factory=list)
    job_types: list[PreferredJobTypeSchema] = Field(default_factory=list)
    job_roles: list[PreferredJobRoleSchema] = Field(default_factory=list)
    industries: list[PreferredIndustrySchema] = Field(default_factory=list)
    skills: list[UserSkillSchema] = Field(default_factory=list)
    technologies: list[UserTechnologySchema] = Field(default_factory=list)
    languages: list[UserLanguageSchema] = Field(default_factory=list)
    preferred_companies: list[PreferredCompanySchema] = Field(default_factory=list)

    model_config = {"from_attributes": True}


class ProfileOutputSchema(BaseModel):
    """Output schema returned by GET and PUT."""

    id: int
    full_name: str | None
    email: str | None
    phone: str | None
    location: str | None
    mobility: str | None
    remote_preference: str | None
    desired_salary_min: int | None
    desired_salary_max: int | None
    availability_date: str | None
    internship_duration_weeks: int | None
    contract_types: list[PreferredContractTypeSchema]
    job_types: list[PreferredJobTypeSchema]
    job_roles: list[PreferredJobRoleSchema]
    industries: list[PreferredIndustrySchema]
    skills: list[UserSkillSchema]
    technologies: list[UserTechnologySchema]
    languages: list[UserLanguageSchema]
    preferred_companies: list[PreferredCompanySchema]

    model_config = {"from_attributes": True}
