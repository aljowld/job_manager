import type { UserSkill } from '../../types/profile';

interface SkillsEditorProps {
  items: UserSkill[];
  onChange: (items: UserSkill[]) => void;
}

export function SkillsEditor({ items, onChange }: SkillsEditorProps) {
  function handleAdd(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const skillName = (formData.get('skill_name') as string).trim();
    const proficiency = (formData.get('proficiency_level') as string).trim() || null;
    const yearsStr = formData.get('years_experience') as string;
    const years = yearsStr ? Number(yearsStr) : null;
    
    if (!skillName) return;

    const normalizedValue = skillName.toLowerCase();
    const exists = items.some((item) => item.skill_name.trim().toLowerCase() === normalizedValue);
    if (exists) {
      alert('This skill already exists.');
      return;
    }

    const newItem: UserSkill = {
      skill_name: skillName,
      proficiency_level: proficiency,
      years_experience: years,
    };

    onChange([...items, newItem]);
    e.currentTarget.reset();
  }

  function handleRemove(index: number) {
    const nextItems = [...items];
    nextItems.splice(index, 1);
    onChange(nextItems);
  }

  return (
    <fieldset className="preference-collection">
      <legend>Skills</legend>
      
      {items.length > 0 && (
        <ul className="preference-list">
          {items.map((item, index) => (
            <li key={index} className="preference-item">
              <span className="preference-item-name">{item.skill_name}</span>
              <span className="preference-item-detail">
                {item.proficiency_level ?? 'Any level'} {item.years_experience !== null ? `(${item.years_experience} yrs)` : ''}
              </span>
              <button type="button" onClick={() => handleRemove(index)} aria-label={`Remove ${item.skill_name}`}>
                Remove
              </button>
            </li>
          ))}
        </ul>
      )}

      <form onSubmit={handleAdd} className="preference-add-form">
        <input type="text" name="skill_name" placeholder="Skill name (e.g. Python)" required />
        <input type="text" name="proficiency_level" placeholder="Level (optional)" />
        <input type="number" name="years_experience" placeholder="Years (optional)" min="0" />
        <button type="submit">Add</button>
      </form>
    </fieldset>
  );
}

