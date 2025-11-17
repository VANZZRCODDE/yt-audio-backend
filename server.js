const express = require("express");
const ytdl = require("ytdl-core");
const cors = require("cors");

const app = express();
app.use(cors());

const PORT = process.env.PORT || 3000;

app.get("/audio", async (req, res) => {
  const url = req.query.url;
  if (!url) return res.status(400).json({ error: "URL YouTube required" });

  try {
    const info = await ytdl.getInfo(url);
    const title = info.videoDetails.title.replace(/[^a-zA-Z0-9 ]/g, "");
    res.setHeader("Content-Disposition", `attachment; filename="${title}.mp3"`);
    res.setHeader("Content-Type", "audio/mpeg");

    ytdl(url, { filter: "audioonly", quality: "highestaudio" }).pipe(res);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Failed to fetch audio" });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
