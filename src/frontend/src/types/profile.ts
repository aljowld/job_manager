export type PreferenceLevel =
  | 'REQUIRED'
  | 'VERY_IMPORTANT'
  | 'IMPORTANT'
  | 'BONUS'
  | 'AVOID'
  | 'EXCLUDED';

export interface PreferredContractType {
  contract_type: string;
  preference_level: PreferenceLevel;
}

export interface PreferredJobType {
  job_type: string;
  preference_level: PreferenceLevel;
}

export interface PreferredJobRole {
  job_role: string;
  preference_level: PreferenceLevel;
}

export interface PreferredIndustry {
  industry: string;
  preference_level: PreferenceLevel;
}

export interface PreferredCompany {
  company_name: string;
  preference_level: PreferenceLevel;
}

export interface UserSkill {
  skill_name: string;
  proficiency_level: string | null;
  years_experience: number | null;
}

export interface UserTechnology {
  technology_name: string;
  proficiency_level: string | null;
  years_experience: number | null;
}

export interface UserLanguage {
  language_name: string;
  proficiency_level: string;
}

export interface ProfileInput {
  full_name: string | null;
  email: string | null;
  phone: string | null;
  location: string | null;
  mobility: string | null;
  remote_preference: string | null;
  desired_salary_min: number | null;
  desired_salary_max: number | null;
  availability_date: string | null;
  internship_duration_weeks: number | null;
  contract_types: PreferredContractType[];
  job_types: PreferredJobType[];
  job_roles: PreferredJobRole[];
  industries: PreferredIndustry[];
  skills: UserSkill[];
  technologies: UserTechnology[];
  languages: UserLanguage[];
  preferred_companies: PreferredCompany[];
}

export interface ProfileOutput extends ProfileInput {
  id: number;
}

