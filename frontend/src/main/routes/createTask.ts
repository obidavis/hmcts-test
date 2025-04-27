import { TaskCreate } from '../types/api';

import axios from 'axios';
import { Application } from 'express';

interface TaskFormData {
  taskTitle: string;
  taskDescription: string;
  taskStatus: string;
  'dueDate-day': string;
  'dueDate-month': string;
  'dueDate-year': string;
}

function validateForm(form: TaskFormData): { isValid: boolean; errors: Record<string, string> } {
  const errors: Record<string, string> = {};
  const { 
    taskTitle, 
    taskStatus, 
    'dueDate-day': day, 
    'dueDate-month': month,
    'dueDate-year': year 
  } = form;

  if (!taskTitle) {
    errors['taskTitle'] = 'Title is required';
  }
  if (!taskStatus) {
    errors['taskStatus'] = 'Status is required';
  }
  try {
    const date = new Date(
      Number.parseInt(year),
      Number.parseInt(month) - 1,
      Number.parseInt(day)
    );
    if (isNaN(date.getTime())) {
      errors['dueDate'] = 'Invalid date';
    }
    if (date < new Date()) {
      errors['dueDate'] = 'Due date must be in the future';
    }
  } catch (error) {
    errors['dueDate'] = 'Invalid date';
  }
  
  return { isValid: Object.keys(errors).length === 0, errors };
}

export default function (app: Application): void {
  app.get('/tasks/create', async (req, res) => {
    try {
      console.log('Creating task');
      res.render('create-task');
    } catch (error) {
      console.error('Error making request:', error);
      res.render('tasks', { tasks: [] });
    }
  });

  app.post('/tasks/create', async (req, res) => {
    const { isValid, errors } = validateForm(req.body as TaskFormData);
    if (!isValid) {
      const errorList = Object.entries(errors).map(([key, value]) => ({
        text: value,
        href: `#${key}`,
      }));
      res.render('create-task', {
        errors,
        errorList,
        data: req.body,
      });
      return;
    } else {
      const task: TaskCreate = {
        title: req.body.taskTitle,
        description: req.body.taskDescription,
        status: req.body.taskStatus,
        due_date: new Date(
          Number.parseInt(req.body['dueDate-year']),
          Number.parseInt(req.body['dueDate-month']) - 1,
          Number.parseInt(req.body['dueDate-day'])
        ).toISOString(),
      };
      try {
        const response = await axios.post(`${process.env.BACKEND_URL}/api/v1/tasks`, task);
        console.log('Task created:', response.data);
        res.redirect('/tasks');
      } catch (error) {
        console.error('Error making request:', error);
        res.render('create-task', {
          errorList: [{
            text: 'Unexpected error creating task',
            href: '#',
          }],
          taskTitle: req.body.taskTitle,
          taskDescription: req.body.taskDescription,
          taskStatus: req.body.taskStatus,
          dueDate: {
            day: req.body['dueDate-day'],
            month: req.body['dueDate-month'],
            year: req.body['dueDate-year'],
          },
        });
      }
    }
  });
}