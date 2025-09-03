// server.js
// first instal node lts version.
// then run 'npm install ws' in terminal to install package.
// then run 'node server.js' remmember to change 'server' part according to js file name.
const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 8080 });

let latestPosition = null;

wss.on('connection', (ws) => {
  // Send latest position on new connection
  if (latestPosition) {
    ws.send(JSON.stringify(latestPosition));
  }

  ws.on('message', (message) => {
    try {
      const obj = JSON.parse(message);
      latestPosition = obj;
      // Broadcast to all connected clients except sender
      wss.clients.forEach(client => {
        if (client !== ws && client.readyState === WebSocket.OPEN) {
          client.send(JSON.stringify(obj));
        }
      });
    } catch (err) {
      console.error("Invalid message:", message);
    }
  });

  ws.on('error', (error) => {
    console.error('WebSocket error:', error);
  });
});

console.log('WebSocket server running on ws://localhost:8080');
