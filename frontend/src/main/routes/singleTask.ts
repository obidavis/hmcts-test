import { Task } from '../types/api';

import axios from 'axios';
import { Application } from 'express';

function formatStatus(status: string): { tag: { text: string; color: string } } {
  switch (status) {
    case 'pending':
      return { tag: { text: 'Pending', color: 'yellow' } };
    case 'in_progress':
      return { tag: { text: 'In Progress', color: 'blue' } };
    case 'completed':
      return { tag: { text: 'Completed', color: 'green' } };
    case 'failed':
      return { tag: { text: 'Failed', color: 'red' } };
    default:
      return { tag: { text: 'Unknown', color: 'grey' } };
  }
}

function formatDate(dateString: string): string {
  const date = new Date(dateString);
  const options: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  };
  return date.toLocaleDateString('en-GB', options);
}


export default function (app: Application): void {
  app.get('/tasks/:id', async (req, res) => {
    try {
      const response = await axios.get(`${process.env.BACKEND_URL}/api/v1/tasks/${req.params.id}`);
      const task: Task = response.data;
      res.render('single-task', { task: {
        id: task.id,
        title: task.title,
        description: task.description,
        status: formatStatus(task.status),
        due_date: formatDate(task.due_date),
      } });
    } catch (error) {
      console.error('Error making request:', error);
      res.render('error');
    }
  });
}