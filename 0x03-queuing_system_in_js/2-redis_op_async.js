import { createClient, print } from 'redis';
import { promisify } from 'util';

const client = createClient();

client.on('connect', () => {
    console.log('Redis client connected to the server');
});

client.on('error', (ERROR_MESSAGE) => {
    console.log(`Redis client not connected to the server: ${ERROR_MESSAGE}`);
});

function setNewSchool(schoolName, value) {
    client.set(schoolName, value, print);
}

const getAsync = promisify(client.get).bind(client);

async function displaySchoolValue(schoolName) {
    const value = await getAsync(schoolName);
	console.log(value);
        }

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
