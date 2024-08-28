import express from 'express';
import redis from 'redis';
import kue from 'kue';
import { promisify } from 'util';

const redisClient = redis.createClient();
const queue = kue.createQueue();

const getAsync = promisify(redisClient.get).bind(redisClient);
const setAsync = promisify(redisClient.set).bind(redisClient);

let reservationEnabled = true;
const INITIAL_SEATS = 50;

const app = express();
const port = 1245;

(async function initializeSeats() {
  await setAsync('available_seats', INITIAL_SEATS);
})();

app.get('/available_seats', async (req, res) => {
  try {
    const seats = await getAsync('available_seats');
    res.json({ numberOfAvailableSeats: seats });
  } catch (err) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  const job = queue.create('reserve_seat').save((error) => {
    if (error) {
      return res.json({ status: 'Reservation failed' });
    }
    res.json({ status: 'Reservation in process' });
  });

  job.on('complete', (result) => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (errorMessage) => {
    console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
  });
});

app.get('/process', async (req, res) => {
  queue.process('reserve_seat', async (job, done) => {
    try {
      const availableSeats = parseInt(await getAsync('available_seats'), 10);

      if (availableSeats > 0) {
        await setAsync('available_seats', availableSeats - 1);
        if (availableSeats - 1 === 0) {
          reservationEnabled = false;
        }
        done();
      } else {
        done(new Error('Not enough seats available'));
      }
    } catch (err) {
      done(err);
    }
  });

  res.json({ status: 'Queue processing' });
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});

