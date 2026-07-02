import { useState } from 'react';

interface TodoItem {
  id: number;
  text: string;
}

export default function App() {
  const [items, setItems] = useState<TodoItem[]>([
    { id: 1, text: 'Learn React' },
    { id: 2, text: 'Learn TypeScript' }
  ]);
  const [inputValue, setInputValue] = useState<string>('');

  const handleAddItem = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const newItem: TodoItem = {
      id: Date.now(), 
      text: inputValue
    };

    setItems([...items, newItem]);
    setInputValue('');
  };

  return (
    <div>      
      <form onSubmit={handleAddItem}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Add a new task..."
        />
        <button type="submit">Add</button>
      </form>

      <ul>
        {items.map((item) => (
          <li key={item.id}>{item.text}</li>
        ))}
      </ul>
    </div>
  );
}
