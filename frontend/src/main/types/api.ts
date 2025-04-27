export type Task = {
  id: number;
  title: string;
  description?: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  due_date: string;
}

export type TaskCreate = {
  title: string;
  description?: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  due_date: string;
}