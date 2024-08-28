import express from 'express';
import redis from 'redis';
import { promisify } from 'util';

const app = express();
const port = 1245;

const redisClient = redis.createClient();
const getAsync = promisify(redisClient.get).bind(redisClient);
const setAsync = promisify(redisClient.set).bind(redisClient);

const listProducts = [
    { id: 1, name: 'Suitcase 250', price: 50, stock: 4 },
    { id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
    { id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
    { id: 4, name: 'Suitcase 1050', price: 550, stock: 5 }
];

function getItemById(id) {
    return listProducts.find(product => product.id === id);
}

app.get('/list_products', (req, res) => {
    res.json(listProducts.map(({ id, name, price, stock }) => ({
        itemId: id,
        itemName: name,
        price,
        initialAvailableQuantity: stock
    })));
});

app.get('/list_products/:itemId', async (req, res) => {
    const itemId = parseInt(req.params.itemId, 10);
    const product = getItemById(itemId);
    if (!product) {
        return res.status(404).json({ status: 'Product not found' });
    }

    const reservedStock = await getAsync(`item.${itemId}`);
    const currentQuantity = product.stock - (reservedStock ? parseInt(reservedStock, 10) : 0);

    res.json({ ...product, currentQuantity });
});

app.get('/reserve_product/:itemId', async (req, res) => {
    const itemId = parseInt(req.params.itemId, 10);
    const product = getItemById(itemId);
    if (!product) {
        return res.status(404).json({ status: 'Product not found' });
    }

    const reservedStock = await getAsync(`item.${itemId}`);
    const currentQuantity = product.stock - (reservedStock ? parseInt(reservedStock, 10) : 0);

    if (currentQuantity <= 0) {
        return res.json({ status: 'Not enough stock available', itemId });
    }

    await setAsync(`item.${itemId}`, (reservedStock ? parseInt(reservedStock, 10) : 0) + 1);
    res.json({ status: 'Reservation confirmed', itemId });
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});

