const { onRequest } = require("firebase-functions/v2/https");
const neo4j = require("neo4j-driver");
const cors = require("cors")({ origin: true });

const uri = "neo4j+s://6095dc87.databases.neo4j.io:7687";
const user = "neo4j";
const password = "APGMB_0ZIYaw8PFXq_Cy3utL7AoEClikHFR-xMaxk2E";

const driver = neo4j.driver(uri, neo4j.auth.basic(user, password), {
  disableLosslessIntegers: true
});

exports.queryCitationNetwork = onRequest((req, res) => {
    cors(req, res, async () => {
        const session = driver.session();
        const { titleOrDoi, depth, citationDirection } = req.body;

        if (!titleOrDoi || !depth) {
            res.status(400).send("Both title/DOI and depth must be provided.");
            return;
        }

        const maxDepth = Math.min(parseInt(depth), 5);
        const direction = citationDirection || "CITES>"; // Default to "CITES>"

        const query = `
            MATCH (p:Paper)
            WHERE p.title = $titleOrDoi OR p.doi = $titleOrDoi
            CALL apoc.path.subgraphAll(p, {
                maxLevel: $depth,
                relationshipFilter: "${direction}"
            })
            YIELD nodes, relationships
            RETURN nodes, relationships
        `;

        try {
            const result = await session.run(query, { titleOrDoi, depth: maxDepth });
            const nodes = result.records[0].get('nodes').map(node => ({
                ...node.properties,
                neo4j_id: node.identity
            }));
            const relationships = result.records[0].get('relationships').map(rel => ({
                start: rel.start,
                end: rel.end,
                type: rel.type
            }));

            res.status(200).json({ nodes, relationships });
        } catch (error) {
            console.error(error);
            res.status(500).send("Error querying Neo4j");
        } finally {
            await session.close();
        }
    });
});


exports.queryVenueImpact = onRequest((req, res) => {
    cors(req, res, async () => {
        const session = driver.session();
        const { venueName } = req.body;

        if (!venueName) {
            res.status(400).send("Venue name must be provided.");
            return;
        }

        const query = `
            MATCH (v:Venue {name: $venueName})<-[:PUBLISHED_IN]-(p:Paper)-[:HAS_FOS]->(fos:FieldOfStudy)
            RETURN v.name AS Venue, fos.name AS FieldOfStudy, count(p) AS PapersPublished
            ORDER BY PapersPublished DESC
        `;

        try {
            const result = await session.run(query, { venueName });
            const records = result.records.map(record => record.toObject());
            console.log("Venue Impact Query Results: ", records);
            res.status(200).json(records);
        } catch (error) {
            console.error(error);
            res.status(500).send("Error querying Neo4j");
        } finally {
            await session.close();
        }
    });
});

exports.queryInfluentialAuthors = onRequest((req, res) => {
    cors(req, res, async () => {
        const session = driver.session();
        const { fieldName } = req.body;

        if (!fieldName) {
            res.status(400).send("Field name must be provided.");
            return;
        }

        const query = `
            MATCH (a:Author)-[:AUTHORED]->(p:Paper)-[:HAS_FOS]->(f:FieldOfStudy)
            WHERE f.name = $fieldName
            RETURN a.name AS Author, COUNT(p) AS Papers
            ORDER BY Papers DESC
            LIMIT 10
        `;

        try {
            const result = await session.run(query, { fieldName });
            const records = result.records.map(record => record.toObject());
            console.log("Influential Authors Query Results: ", records);
            res.status(200).json(records);
        } catch (error) {
            console.error(error);
            res.status(500).send("Error querying Neo4j");
        } finally {
            await session.close();
        }
    });
});
