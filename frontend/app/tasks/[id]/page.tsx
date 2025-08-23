'use client';
import { useEffect, useState } from 'react';
import { getTask } from '@/lib/api';

export default function TaskDetails({ params }: { params: { id: string } }) {
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token') || '';
    let cancelled = false;
    async function poll() {
      try {
        const res = await getTask(token, Number(params.id));
        if (!cancelled) setData(res);
        if (res.status !== 'succeeded' && res.status !== 'failed') {
          setTimeout(poll, 800);
        } else {
          setLoading(false);
        }
      } catch (e: any) {
        if (!cancelled) {
          setError(e.message || 'Failed to fetch task');
          setLoading(false);
        }
      }
    }
    poll();
    return () => { cancelled = true; };
  }, [params.id]);

  return (
    <div>
      <h2>Task {params.id}</h2>
      {loading && <div>Loading...</div>}
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {data && (
        <pre style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(data, null, 2)}</pre>
      )}
    </div>
  );
}
