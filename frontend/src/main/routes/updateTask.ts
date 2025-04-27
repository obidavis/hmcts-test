import axios from 'axios';
import { Application } from 'express';

export default function (app: Application): void {
  app.get('/tasks/:id/update', async (req, res) => {
    try {
      const { data } = await axios.get(`${process.env.BACKEND_URL}/api/v1/tasks/${req.params.id}`);
      const dateString = new Date(data.due_date).toLocaleDateString('en-GB', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
      });
      res.render('update-task', {
        task: {
          id: data.id,
          title: data.title,
          description: data.description,
          status: data.status,
          due_date: dateString,
        },
      });
    } catch (error) {
      console.error('Error making request:', error);
      res.render('error');
    }
  });

  app.post('/tasks/:id/update', async (req, res) => {
    const updatedTask = {
      status: req.body.taskStatus,
    };
    try {
      await axios.patch(`${process.env.BACKEND_URL}/api/v1/tasks/${req.params.id}`, updatedTask);
      res.redirect(`/tasks/${req.params.id}`);
    } catch (error) {
      console.error('Error making request:', error);
      res.render('error');
    }
  });
}