const express = require('express');
const app = express();
const port = process.env.PORT || 3000;
const Cloudant = require('@cloudant/cloudant');

// Initialize Cloudant connection with IAM authentication
async function dbCloudantConnect() {
    try {
        const cloudant = Cloudant({
            plugins: { iamauth: { iamApiKey: '4XjngQA0CruDZEjW5OwF1A6GJf-BZ80IXxWSWgHQ-2A2' } }, // Replace with your IAM API key
            url: 'https://866d0059-4d39-44a4-926f-702c3f1e363b-bluemix.cloudantnosqldb.appdomain.cloud', // Replace with your Cloudant URL
        });

        const db = cloudant.use('dealerships');
        console.info('Connect success! Connected to DB');
        return db;
    } catch (err) {
        console.error('Connect failure: ' + err.message + ' for Cloudant DB');
        throw err;
    }
}

let db;

(async () => {
    db = await dbCloudantConnect();
})();

app.use(express.json());

// Define a route to get all dealerships with optional state and ID filters

app.get('/dealerships/get', (req, res) => {
    const { id } = req.query;

    // Check if the "id" parameter is provided
    if (id) {
        // If "id" is provided, retrieve a specific dealer by "id"
        const selector = { id: parseInt(id) }; // Assuming "id" is an integer
        const queryOptions = {
            selector,
            limit: 1 // Limit to 1 result since "id" should be unique
        };

        // Query the Cloudant database with the selector and options
        db.find(queryOptions, (err, body) => {
            if (err) {
                console.error('Error fetching dealership by id:', err);
                res.status(500).json({ error: 'An error occurred while fetching the dealership.' });
            } else {
                if (body.docs.length === 0) {
                    res.status(404).json({ error: 'Dealer not found.' });
                } else {
                    res.json(body.docs[0]);
                }
            }
        });
    } else {
        // If "id" is not provided, fetch all dealerships
        const queryOptions = {
            selector: {},
            limit: 20 // Limit to 15 results (adjust as needed)
        };

        // Query the Cloudant database to retrieve all dealerships
        db.find(queryOptions, (err, body) => {
            if (err) {
                console.error('Error fetching dealerships:', err);
                res.status(500).json({ error: 'An error occurred while fetching dealerships.' });
            } else {
                const dealerships = body.docs;
                res.json(dealerships);
            }
        });
    }
});

// app.get('/dealerships/get', (req, res) => {
//     const { state, id } = req.query;

//     // Create a selector object based on query parameters
//     const selector = {};
//     if (state) {
//         selector.state = state;
//     }
//     if (id) {
//         console.log(`id: ${id}`)
        
//         selector.id = id;
//         console.log(`selector: ${JSON.stringify(selector)}`)
//     }

//     const queryOptions = {
//         selector,
//         limit: 15, // Limit the number of documents returned to 10
//     };

//     db.find(queryOptions, (err, body) => {
//         if (err) {
//             console.error('Error fetching dealerships:', err);
//             res.status(500).json({ error: 'An error occurred while fetching dealerships.' });
//         } else {
//             const dealerships = body.docs;
//             res.json(dealerships);
//         }
//     });
// });

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});