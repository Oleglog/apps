const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

let userCounter = 1;

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

io.on('connection', (socket) => {
    const userName = `Пользователь ${userCounter++}`;
    socket.userName = userName;

    console.log(`${userName} подключился`);

    // Личное сообщение новому пользователю
    socket.emit('chat message', {
        user: 'Система',
        text: `Добро пожаловать ${userName}`
    });

    // Уведомление остальных
    socket.broadcast.emit('chat message', {
        user: 'Система',
        text: `${userName} вошёл в чат`
    });

    socket.on('chat message', (msg) => {
        if (!msg || !msg.trim()) return;

        io.emit('chat message', {
            user: socket.userName,
            text: msg
        });
    });

    socket.on('disconnect', () => {
        socket.broadcast.emit('chat message', {
            user: 'Система',
            text: `${socket.userName} вышел из чата`
        });
    });
});

server.listen(3000, () => {
    console.log('Сервер запущен: http://localhost:3000');
});