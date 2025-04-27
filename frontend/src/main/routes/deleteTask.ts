import axios from 'axios';
import { Application } from 'express';

export default function (app: Application): void {
  app.post('/tasks/:id/delete', async (req, res) => {
    try {
      await axios.delete(`http://localhost:8000/api/v1/tasks/${req.params.id}`);
      res.redirect('/tasks');
    } catch (error) {
      console.error('Error making request:', error);
      res.render('error');
    }
  });
}