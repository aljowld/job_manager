import type { UserLanguage } from '../../types/profile';

interface LanguagesEditorProps {
  items: UserLanguage[];
  onChange: (items: UserLanguage[]) => void;
}

export function LanguagesEditor({ items, onChange }: LanguagesEditorProps) {
  function handleAdd(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const langName = (formData.get('language_name') as string).trim();
    const proficiency = (formData.get('proficiency_level') as string).trim();
    
    if (!langName || !proficiency) return;

    const normalizedValue = langName.toLowerCase();
    const exists = items.some((item) => item.language_name.trim().toLowerCase() === normalizedValue);
    if (exists) {
      alert('This language already exists.');
      return;
    }

    const newItem: UserLanguage = {
      language_name: langName,
      proficiency_level: proficiency,
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
      <legend>Languages</legend>
      
      {items.length > 0 && (
        <ul className="preference-list">
          {items.map((item, index) => (
            <li key={index} className="preference-item">
              <span className="preference-item-name">{item.language_name}</span>
              <span className="preference-item-detail">{item.proficiency_level}</span>
              <button type="button" onClick={() => handleRemove(index)} aria-label={`Remove ${item.language_name}`}>
                Remove
              </button>
            </li>
          ))}
        </ul>
      )}

      <form onSubmit={handleAdd} className="preference-add-form">
        <input type="text" name="language_name" placeholder="Language (e.g. English)" required />
        <input type="text" name="proficiency_level" placeholder="Level (e.g. Fluent)" required />
        <button type="submit">Add</button>
      </form>
    </fieldset>
  );
}

