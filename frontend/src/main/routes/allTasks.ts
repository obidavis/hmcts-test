import { Task } from '../types/api';

import axios from 'axios';
import { Application } from 'express';

export default function (app: Application): void {
  app.get('/tasks', async (req, res) => {
    try {
      const response = await axios.get('http://localhost:8000/api/v1/tasks');
      const tasks: Task[] = response.data;
      res.render('all-tasks', { tasks: tasks.map(task => ({
        title: {
          text: task.title,
        },
        href: `/tasks/view/${task.id}`,
        status: {
          tag: {
            text: task.status,
            color: task.status === 'completed' ? 'green' : 'red',
          }
        }
      })) });
    } catch (error) {
      console.error('Error making request:', error);
      res.render('allTasks', { tasks: [] });
    }
  });
}