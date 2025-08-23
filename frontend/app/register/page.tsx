'use client';
import { useState } from 'react';
import { register } from '@/lib/api';

export default function RegisterPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      const data = await register(email, password, fullName);
      localStorage.setItem('token', data.access_token);
      window.location.href = '/dashboard';
    } catch (e: any) {
      setError(e.message || 'Register failed');
    }
  }

  return (
    <div>
      <h2>Register</h2>
      <form onSubmit={onSubmit} style={{ display: 'grid', gap: 8, maxWidth: 320 }}>
        <input placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
        <input placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
        <input placeholder="Full Name" value={fullName} onChange={e => setFullName(e.target.value)} />
        <button type="submit">Create account</button>
        {error && <div style={{ color: 'red' }}>{error}</div>}
      </form>
    </div>
  );
}
