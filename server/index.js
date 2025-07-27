const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const rateLimit = require('express-rate-limit');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-in-production';

// Middleware
app.use(cors());
app.use(express.json());

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});
app.use(limiter);

// Database setup
const db = new sqlite3.Database('./database.sqlite');

// Initialize database tables
db.serialize(() => {
  // Users table
  db.run(`CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )`);

  // Sample data table
  db.run(`CREATE TABLE IF NOT EXISTS sample_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    value REAL NOT NULL,
    status TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )`);

  // Chat messages table
  db.run(`CREATE TABLE IF NOT EXISTS chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    response TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
  )`);

  // Insert sample data if table is empty
  db.get("SELECT COUNT(*) as count FROM sample_data", (err, row) => {
    if (!err && row.count === 0) {
      const sampleData = [
        ['Product A', 'Electronics', 299.99, 'Active'],
        ['Product B', 'Clothing', 49.99, 'Active'],
        ['Product C', 'Books', 19.99, 'Inactive'],
        ['Product D', 'Electronics', 899.99, 'Active'],
        ['Product E', 'Home & Garden', 129.99, 'Active'],
        ['Product F', 'Sports', 79.99, 'Active'],
        ['Product G', 'Electronics', 199.99, 'Inactive'],
        ['Product H', 'Clothing', 89.99, 'Active'],
        ['Product I', 'Books', 24.99, 'Active'],
        ['Product J', 'Home & Garden', 159.99, 'Active']
      ];

      const stmt = db.prepare("INSERT INTO sample_data (name, category, value, status) VALUES (?, ?, ?, ?)");
      sampleData.forEach(data => {
        stmt.run(data);
      });
      stmt.finalize();
    }
  });

  // Create default admin user if no users exist
  db.get("SELECT COUNT(*) as count FROM users", (err, row) => {
    if (!err && row.count === 0) {
      const hashedPassword = bcrypt.hashSync('admin123', 10);
      db.run("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", 
        ['admin', hashedPassword, 'admin@example.com']);
    }
  });
});

// Auth middleware
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.sendStatus(401);
  }

  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err) return res.sendStatus(403);
    req.user = user;
    next();
  });
};

// Routes
app.post('/api/login', (req, res) => {
  const { username, password } = req.body;

  db.get("SELECT * FROM users WHERE username = ?", [username], (err, user) => {
    if (err) {
      return res.status(500).json({ error: 'Database error' });
    }

    if (!user || !bcrypt.compareSync(password, user.password)) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    const token = jwt.sign({ id: user.id, username: user.username }, JWT_SECRET);
    res.json({ token, user: { id: user.id, username: user.username, email: user.email } });
  });
});

app.post('/api/register', (req, res) => {
  const { username, password, email } = req.body;

  if (!username || !password || !email) {
    return res.status(400).json({ error: 'All fields are required' });
  }

  const hashedPassword = bcrypt.hashSync(password, 10);

  db.run("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", 
    [username, hashedPassword, email], function(err) {
    if (err) {
      if (err.message.includes('UNIQUE constraint failed')) {
        return res.status(400).json({ error: 'Username or email already exists' });
      }
      return res.status(500).json({ error: 'Database error' });
    }

    const token = jwt.sign({ id: this.lastID, username }, JWT_SECRET);
    res.json({ token, user: { id: this.lastID, username, email } });
  });
});

app.get('/api/data', authenticateToken, (req, res) => {
  db.all("SELECT * FROM sample_data ORDER BY created_at DESC", (err, rows) => {
    if (err) {
      return res.status(500).json({ error: 'Database error' });
    }
    res.json(rows);
  });
});

app.get('/api/chat/history', authenticateToken, (req, res) => {
  db.all("SELECT * FROM chat_messages WHERE user_id = ? ORDER BY created_at ASC", 
    [req.user.id], (err, rows) => {
    if (err) {
      return res.status(500).json({ error: 'Database error' });
    }
    res.json(rows);
  });
});

app.post('/api/chat', authenticateToken, async (req, res) => {
  const { message } = req.body;

  if (!message) {
    return res.status(400).json({ error: 'Message is required' });
  }

  try {
    // Simple AI response simulation - replace with actual AI service
    const response = await generateAIResponse(message);

    // Save to database
    db.run("INSERT INTO chat_messages (user_id, message, response) VALUES (?, ?, ?)",
      [req.user.id, message, response], function(err) {
      if (err) {
        return res.status(500).json({ error: 'Database error' });
      }

      res.json({ 
        id: this.lastID,
        message, 
        response,
        created_at: new Date().toISOString()
      });
    });
  } catch (error) {
    res.status(500).json({ error: 'AI service error' });
  }
});

// Simple AI response simulation
async function generateAIResponse(message) {
  // This is a simple simulation - replace with actual AI service like OpenAI
  const responses = [
    "That's an interesting question! Let me think about that.",
    "I understand what you're asking. Here's my perspective:",
    "Based on the data I can see, I would suggest:",
    "That's a great point! Here's what I think:",
    "I can help you with that. My recommendation would be:",
    "Thank you for asking! From my analysis:"
  ];

  const randomResponse = responses[Math.floor(Math.random() * responses.length)];
  
  // Add some context based on the message
  if (message.toLowerCase().includes('data') || message.toLowerCase().includes('table')) {
    return `${randomResponse} Looking at your data table, I can see various products across different categories. Would you like me to analyze any specific aspect of this data?`;
  } else if (message.toLowerCase().includes('product')) {
    return `${randomResponse} I notice you have several products in your database. The electronics category seems to be well-represented. Is there something specific about the products you'd like to explore?`;
  } else {
    return `${randomResponse} ${message.charAt(0).toUpperCase() + message.slice(1)} is definitely worth considering. What would you like to know more about?`;
  }
}

// Serve static files in production
if (process.env.NODE_ENV === 'production') {
  app.use(express.static(path.join(__dirname, '../client/build')));
  
  app.get('*', (req, res) => {
    if (!req.path.startsWith('/api')) {
      res.sendFile(path.join(__dirname, '../client/build', 'index.html'));
    }
  });
}

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
}); 