import type { Task, TaskEvent } from '@autumn/sdk';

export interface Bridge {
  connection(): Promise<{mode: string; workspace: string}>;
  tasks(): Promise<Task[]>;
  submit(key: string): Promise<Task>;
  events(id: string, after: number): Promise<TaskEvent[]>;
}
