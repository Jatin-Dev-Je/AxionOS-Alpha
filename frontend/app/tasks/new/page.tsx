'use client';
import { useState } from 'react';
import { createTask } from '@/lib/api';

export default function NewTaskPage() {
  const [type, setType] = useState('knowledge_query');
  const [q, setQ] = useState('What is AxionOS?');
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    const token = localStorage.getItem('token') || '';
    try {
      const res = await createTask(token, type, type === 'knowledge_query' ? { q } : { messages: [{ role: 'user', content: q }] });
      setResult(res);
    } catch (e: any) {
      setError(e.message || 'Failed to create task');
    }
  }

  return (
    <div>
      <h2>New Task</h2>
      <form onSubmit={onSubmit} style={{ display: 'grid', gap: 8, maxWidth: 480 }}>
        <select value={type} onChange={e => setType(e.target.value)}>
          <option value="knowledge_query">knowledge_query</option>
          <option value="llm_chat">llm_chat</option>
        </select>
        <textarea value={q} onChange={e => setQ(e.target.value)} rows={4} />
        <button type="submit">Create</button>
      </form>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {result && (
        <div style={{ marginTop: 16 }}>
          <div>Task ID: {result.id}</div>
          <a href={`/tasks/${result.id}`}>View Task</a>
        </div>
      )}
    </div>
  );
}
