// OLD
const { chromium } = require("playwright");

// NEW
const { chromium } = require("playwright-chromium");

const app = express();
const PORT = 4000;

function clean(text) {
  if (!text) return "";
  return text.replace(/\s+/g, " ").trim();
}

async function scrapeNerdWallet() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  await page.goto("https://www.nerdwallet.com/the-best-credit-cards", {
    waitUntil: "domcontentloaded",
    timeout: 60000,
  });

  // Grab rows of the card table
  const cards = await page.$$eval("table tbody tr", (rows) =>
    rows.map((row) => {
      const cells = row.querySelectorAll("td");
      return {
        card_name: cells[0]?.innerText.split("\n")[0] || "", // first line in col 1
        issuer: "", // could parse from apply link later
        network: "", // Visa/Mastercard can be parsed from img src if needed
        annual_fee: cells[2]?.innerText || "",
        apr: "", // not visible in this table, may need details page
        intro_apr: cells[3]?.innerText || "",
        intro_apr_months: "",
        reward_rate: cells[4]?.innerText || "",
        categories: "",
        bonus: cells[3]?.innerText || "", // intro offer usually bonus
        bonus_spend_req: "",
        bonus_window_days: "",
        min_limit: "",
        max_limit: "",
        notes: "Scraped from NerdWallet table",
      };
    })
  );

  await browser.close();
  return cards;
}

app.get("/nerdwallet/cards", async (req, res) => {
  try {
    const cards = await scrapeNerdWallet();
    res.json(cards);
  } catch (err) {
    console.error("Scrape error:", err);
    res.status(500).json({ error: "Failed to scrape NerdWallet cards" });
  }
});

app.listen(PORT, () => {
  console.log(
    `✅ NerdWallet scraper running at http://localhost:${PORT}/nerdwallet/cards`
  );
});
