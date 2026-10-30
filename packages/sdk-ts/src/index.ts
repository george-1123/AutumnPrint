import type { components } from './schema';

export type Task = components['schemas']['Task'];
export type TaskEvent = components['schemas']['TaskEvent'];
export class AutumnClient {
  constructor(private baseUrl: string, private token: string) {}
  private async request<T>(path: string, init?: RequestInit): Promise<T> {
    const response = await fetch(new URL(path, this.baseUrl), {
      ...init,
      headers: { Authorization: `Bearer ${this.token}`, 'Content-Type': 'application/json' },
      signal: AbortSignal.timeout(10000)
    });
    if (!response.ok) throw new Error(`Autumn API returned ${response.status}`);
    return response.json() as Promise<T>;
  }
  list() { return this.request<Task[]>('/tasks'); }
  submit(key: string) {
    return this.request<Task>('/tasks/diagnostic', {
      method: 'POST', body: JSON.stringify({ idempotency_key: key })
    });
  }
  events(id: string, after: number) {
    return this.request<TaskEvent[]>(`/tasks/${encodeURIComponent(id)}/events?after=${after}`);
  }
}
