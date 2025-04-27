import { Task } from '../types/api';

import axios from 'axios';
import { Application } from 'express';

function formatStatus(status: string): { tag: { text: string; classes: string } } {
  switch (status) {
    case 'pending':
      return { tag: { text: 'Pending', classes: 'govuk-tag--yellow' } };
    case 'in_progress':
      return { tag: { text: 'In Progress', classes: 'govuk-tag--blue' } };
    case 'completed':
      return { tag: { text: 'Completed', classes: 'govuk-tag--green' } };
    case 'failed':
      return { tag: { text: 'Failed', classes: 'govuk-tag--red' } };
    default:
      return { tag: { text: 'Unknown', classes: 'govuk-tag--grey' } };
  }
}

export default function (app: Application): void {
  app.get('/tasks', async (req, res) => {
    try {
      const response = await axios.get(`${process.env.BACKEND_URL}/api/v1/tasks`);
      const tasks: Task[] = response.data;
      res.render('all-tasks', { tasks: tasks.map(task => ({
        title: {
          text: task.title,
        },
        href: `/tasks/${task.id}`,
        status: formatStatus(task.status),
      })) });
    } catch (error) {
      console.error('Error making request:', error);
      res.render('allTasks', { tasks: [] });
    }
  });
}