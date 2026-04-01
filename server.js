const express = require('express');
const cors = require('cors');
const mysql = require('mysql2');
const bcrypt = require('bcrypt');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'Amina102938.',
  database: 'orderingApp'
});

db.connect((err) => {
  if (err) {
    console.log('Database connection failed:', err);
  } else {
    console.log('Connected to MySQL! ✅');
  }
});

// REGISTER route
app.post('/register', async (req, res) => {
  const { username, email, password } = req.body;

  // Hash the password
  const hashedPassword = await bcrypt.hash(password, 10);

  const sql = 'INSERT INTO users (username, email, password) VALUES (?, ?, ?)';
  db.query(sql, [username, email, hashedPassword], (err, result) => {
    if (err) {
      if (err.code === 'ER_DUP_ENTRY') {
        return res.status(400).json({ message: 'You are already registered! Please log in.' });
      }
      return res.status(500).json({ message: 'Registration failed', error: err });
    }
    res.status(201).json({ message: 'Registration successful! Please log in.' });
  });
});
// LOGIN route
app.post('/login', async (req, res) => {
  const { email, password } = req.body;

  const sql = 'SELECT * FROM users WHERE email = ?';
  db.query(sql, [email], async (err, results) => {
    if (err) return res.status(500).json({ message: 'Server error' });
    
    if (results.length === 0) {
      return res.status(401).json({ message: 'Email not found!' });
    }

    const user = results[0];
    const passwordMatch = await bcrypt.compare(password, user.password);

    if (!passwordMatch) {
      return res.status(401).json({ message: 'Incorrect password!' });
    }

    res.status(200).json({ message: 'Login successful!', username: user.username });
  });
});
app.listen(3000, () => {
  console.log('Server started on http://localhost:3000');
});