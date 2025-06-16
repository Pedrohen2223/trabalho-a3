const express = require('express');
const app = express();
const db = require('./config/database');
const tutorRoutes = require('./routes/tutorRoutes');
const petRoutes = require('./routes/petRoutes');

app.use(express.json());
app.use('/tutores', tutorRoutes);
app.use('/pets', petRoutes);

app.get('/', (req, res) => {
  res.send('API Controle de Vacinação de Pets e Tutores');
});

const PORT = 3000;
db.sync().then(() => {
  app.listen(PORT, () => console.log(`Servidor rodando na porta ${PORT}`));
});
