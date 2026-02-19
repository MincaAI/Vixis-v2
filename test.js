const { MongoClient } = require("mongodb");

async function getTopCompaniesByMarketCap(companyList) {
  const uri =
    "mongodb+srv://contact:8ofqfJgpsX2qC2aW@cluster0.u30sb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"; // Replace with your MongoDB URI
  const client = new MongoClient(uri);

  try {
    await client.connect();
    const db = client.db("Vixis"); // Replace with your database name
    const collection = db.collection("stock"); // Replace with your collection name

    // Projection to fetch only the required fields
    const projection = {
      _id: 0, // Exclude MongoDB ObjectId
      TICKER: 1, // Column B
      NAME: 1, // Column C
      UNIVERS: 1, // New field for universe
      "PERF YTD (%)": 1, // Column N
      EQY_REC_CONS: 1, // Column E
      BDVD_PROJ_DIV_AMT: 1, // Column J
      IS_DIV_PER_SHR: 1, // Column I
      LOW_52WEEK: 1, // Column K
      HIGH_52WEEK: 1, // Column L
      CUR_MKT_CAP: 1, // Used for sorting
      SCORING: 1, // Column S (VIXIS Scoring)
      PX_LAST: 1, // Column D
      BEST_TARGET_PRICE: 1, // Column F
    };

    // Process input to extract NAME and UNIVERS
    const companies = companyList.split(",").map((entry) => {
      entry = entry.trim();
      const match = entry.match(/(.*)\s\((.*?)\)$/); // Match "AXA (CAC 40)"
      if (match) {
        return { NAME: match[1].toUpperCase(), UNIVERS: match[2] };
      } else {
        return { NAME: entry.toUpperCase(), UNIVERS: null }; // No universe specified
      }
    });

    console.log("Processed companies:", companies);

    var limit = Math.min(companies.length, 3); // Ensure limit does not exceed available companies

    // Build query conditions based on available data
    const queryConditions = companies.map(({ NAME, UNIVERS }) =>
      UNIVERS ? { NAME, UNIVERS } : { NAME }
    );

    // Query MongoDB for matching companies
    const topCompanies = await collection
      .find({ $or: queryConditions }, { projection }) // Match NAME and optionally UNIVERS
      .sort({ CUR_MKT_CAP: -1 }) // Sort in descending order
      .limit(limit) // Get top N companies
      .toArray();

    // Use Promise.all to fetch API data concurrently
    const enrichedCompanies = await Promise.all(
      topCompanies.map(async (company, index) => {
        company.RANK = index + 1;

        try {
          const response = await fetch(
            `https://company-query.onrender.com/query?company_name=${encodeURIComponent(
              company.NAME
            )}`
          );
          const apiData = await response.json(); // Parse API response

          return { ...company, ...apiData }; // Merge MongoDB and API data
        } catch (error) {
          console.error(`Failed to fetch data for ${company.NAME}:`, error);
          return company; // Return original company data if API call fails
        }
      })
    );

    console.log("Enriched companies:", enrichedCompanies);
    return "Top 3 Companies by Market Cap:", topCompanies;
  } catch (error) {
    console.error("Error fetching companies:", error);
  } finally {
    await client.close();
  }
}

// Example usage
const companyString =
  "STELLANTIS, ENGIE, BNP PARIBAS, AXA (CAC 40), VOLKSWAGEN";
console.log(getTopCompaniesByMarketCap(companyString));
