const express = require("express");
const cors = require("cors"); // Import cors
const fs = require("fs");
const path = require("path");

const app = express();

// Enable CORS for all origins
app.use(cors());

// Parse JSON requests
app.use(express.json());

// Path to the rules.json file
const filePath = path.join(__dirname, "rules.json");

// API to get all rules
app.get("/api/rules", (req, res) => {
  fs.readFile(filePath, "utf8", (err, data) => {
    if (err) {
      return res.status(500).json({ error: "Failed to read rules file" });
    }
    res.json(JSON.parse(data || "[]"));
  });
});

// API to save rules
app.post("/api/rules", (req, res) => {
  const rules = req.body;
  fs.writeFile(filePath, JSON.stringify(rules, null, 2), "utf8", (err) => {
    if (err) {
      return res.status(500).json({ error: "Failed to save rules" });
    }
    res.status(200).json({ message: "Rules saved successfully" });
  });
});

// Start the server
const PORT = 3001;
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
