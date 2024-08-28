import { expect } from 'chai';
import kue from 'kue';
import createPushNotificationsJobs from './8-job.js';

describe('createPushNotificationsJobs', function() {
    let queue;

    beforeEach(() => {
        queue = kue.createQueue();
        queue.testMode.enter();
    });

    afterEach(() => {
	queue.testMode.exit();
    });

    it('should throw an error if jobs is not an array', () => {
        expect(() => createPushNotificationsJobs({}, queue)).to.throw('Jobs is not an array');
    });

    it('should create jobs and log correct messages', (done) => {
        const list = [
            { phoneNumber: '4153518780', message: 'Test message' }
        ];

        createPushNotificationsJobs(list, queue);

        const job = queue.testMode.jobs[0];
        expect(queue.testMode.jobs.length).to.equal(1);
        expect(job.type).to.equal('push_notification_code_3');
        done();
    });
});

