import type { PreferenceLevel } from '../../types/profile';

interface PreferenceCollectionEditorProps<T> {
  title: string;
  items: T[];
  itemKey: keyof T;
  onChange: (items: T[]) => void;
}

export function PreferenceCollectionEditor<T extends { preference_level: PreferenceLevel }>({
  title,
  items,
  itemKey,
  onChange,
}: PreferenceCollectionEditorProps<T>) {
  function handleAdd(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const newValue = formData.get('value') as string;
    const newLevel = formData.get('preference_level') as PreferenceLevel;
    
    if (!newValue.trim()) return;

    const normalizedValue = newValue.trim().toLowerCase();
    const exists = items.some((item) => String(item[itemKey]).trim().toLowerCase() === normalizedValue);
    if (exists) {
      alert('This item already exists.');
      return;
    }

    const newItem = {
      [itemKey]: newValue.trim(),
      preference_level: newLevel,
    } as unknown as T;

    onChange([...items, newItem]);
    e.currentTarget.reset();
  }

  function handleRemove(index: number) {
    const nextItems = [...items];
    nextItems.splice(index, 1);
    onChange(nextItems);
  }

  function handleLevelChange(index: number, newLevel: PreferenceLevel) {
    const nextItems = [...items];
    nextItems[index] = { ...nextItems[index], preference_level: newLevel };
    onChange(nextItems);
  }

  return (
    <fieldset className="preference-collection">
      <legend>{title}</legend>
      
      {items.length > 0 && (
        <ul className="preference-list">
          {items.map((item, index) => (
            <li key={index} className="preference-item">
              <span className="preference-item-name">{String(item[itemKey])}</span>
              <select
                value={item.preference_level}
                onChange={(e) => handleLevelChange(index, e.target.value as PreferenceLevel)}
                aria-label={`Preference level for ${String(item[itemKey])}`}
              >
                <option value="REQUIRED">REQUIRED</option>
                <option value="VERY_IMPORTANT">VERY_IMPORTANT</option>
                <option value="IMPORTANT">IMPORTANT</option>
                <option value="BONUS">BONUS</option>
                <option value="AVOID">AVOID</option>
                <option value="EXCLUDED">EXCLUDED</option>
              </select>
              <button type="button" onClick={() => handleRemove(index)} aria-label={`Remove ${String(item[itemKey])}`}>
                Remove
              </button>
            </li>
          ))}
        </ul>
      )}

      <form onSubmit={handleAdd} className="preference-add-form">
        <input type="text" name="value" placeholder="Add new item..." required />
        <select name="preference_level" required>
          <option value="IMPORTANT">IMPORTANT</option>
          <option value="REQUIRED">REQUIRED</option>
          <option value="VERY_IMPORTANT">VERY_IMPORTANT</option>
          <option value="BONUS">BONUS</option>
          <option value="AVOID">AVOID</option>
          <option value="EXCLUDED">EXCLUDED</option>
        </select>
        <button type="submit">Add</button>
      </form>
    </fieldset>
  );
}

