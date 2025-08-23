'use client';
import useSWR from 'swr';
import { me } from '@/lib/api';

export default function Dashboard() {
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') || '' : '';
  const { data, error, isLoading } = useSWR(token ? ['me', token] : null, ([_, t]) => me(t));

  return (
    <div>
      <h2>Dashboard</h2>
      {!token && <div>Please login.</div>}
      {isLoading && <div>Loading...</div>}
      {error && <div style={{ color: 'red' }}>{String(error)}</div>}
      {data && (
        <div>
          <div>Email: {data.email}</div>
          <button onClick={() => { localStorage.removeItem('token'); window.location.href = '/login'; }}>Logout</button>
        </div>
      )}
    </div>
  );
}
