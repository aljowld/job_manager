import type { UserTechnology } from '../../types/profile';

interface TechnologiesEditorProps {
  items: UserTechnology[];
  onChange: (items: UserTechnology[]) => void;
}

export function TechnologiesEditor({ items, onChange }: TechnologiesEditorProps) {
  function handleAdd(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const techName = (formData.get('technology_name') as string).trim();
    const proficiency = (formData.get('proficiency_level') as string).trim() || null;
    const yearsStr = formData.get('years_experience') as string;
    const years = yearsStr ? Number(yearsStr) : null;
    
    if (!techName) return;

    const normalizedValue = techName.toLowerCase();
    const exists = items.some((item) => item.technology_name.trim().toLowerCase() === normalizedValue);
    if (exists) {
      alert('This technology already exists.');
      return;
    }

    const newItem: UserTechnology = {
      technology_name: techName,
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
      <legend>Technologies</legend>
      
      {items.length > 0 && (
        <ul className="preference-list">
          {items.map((item, index) => (
            <li key={index} className="preference-item">
              <span className="preference-item-name">{item.technology_name}</span>
              <span className="preference-item-detail">
                {item.proficiency_level ?? 'Any level'} {item.years_experience !== null ? `(${item.years_experience} yrs)` : ''}
              </span>
              <button type="button" onClick={() => handleRemove(index)} aria-label={`Remove ${item.technology_name}`}>
                Remove
              </button>
            </li>
          ))}
        </ul>
      )}

      <form onSubmit={handleAdd} className="preference-add-form">
        <input type="text" name="technology_name" placeholder="Tech name (e.g. React)" required />
        <input type="text" name="proficiency_level" placeholder="Level (optional)" />
        <input type="number" name="years_experience" placeholder="Years (optional)" min="0" />
        <button type="submit">Add</button>
      </form>
    </fieldset>
  );
}

