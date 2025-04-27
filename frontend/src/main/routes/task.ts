import { Task } from '../types/api';

import axios from 'axios';
import { Application } from 'express';

export default function (app: Application): void {
  app.get('/tasks/:id', async (req, res) => {
    try {
      const response = await axios.get(`http://localhost:8000/api/v1/tasks/${req.params.id}`);
      const task: Task = response.data;
      res.render('task', { task });
    } catch (error) {
      console.error('Error making request:', error);
      res.render('error');
    }
  });
}