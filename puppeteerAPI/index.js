import express from 'express';
import { CreateEvent, setAttendees } from './puppeteerFunctions.js';

const app = express();

app.post('/creatEvent', async (req, res) => {
  const { clubID, clubPassword, eventName, location, startDate, endDate } =
    req.body;
  try {
    const response = await CreateEvent(
      clubID,
      clubPassword,
      eventName,
      location,
      startDate,
      endDate
    );
    if (response === 'success') {
      res.status(200).send(response);
    } else if (response === 'loginFail') {
      res.status(401);
    }
  } catch (e) {
    res.status(500).send(e);
  }
});

app.post('/setAttendees', async (req, res) => {
  const { clubID, clubPassword, studentIDs } = req.body;
  try {
    const response = await setAttendees(clubID, clubPassword, studentIDs);
    if (response === 'success') {
      res.status(200).send(response);
    } else if (response === 'loginFail') {
      res.status(401);
    }
  } catch (e) {
    res.status(500).send(e);
  }
});

export const run = app;
