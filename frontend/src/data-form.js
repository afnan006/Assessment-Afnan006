import { useState } from 'react';
import {
    Box,
    Button,
    Typography,
    TextField,
} from '@mui/material';
import axios from 'axios';

const endpointMapping = {
    'Notion': 'notion',
    'Airtable': 'airtable',
    'HubSpot': 'hubspot', // Ensure HubSpot is included
};

export const DataForm = ({ integrationType, credentials }) => {
    const [loadedData, setLoadedData] = useState(null);
    const [error, setError] = useState(null);

    const handleLoad = async () => {
        try {
            const formData = new FormData();
            formData.append('credentials', JSON.stringify(credentials));
            formData.append('user_id', 'TestUser'); // Replace with actual user ID
            formData.append('org_id', '49173978');  // Replace with your HubSpot Account ID

            const response = await axios.post(
                `http://localhost:8000/integrations/${endpointMapping[integrationType]}/load`,
                formData
            );

            // Store the fetched data in a readable JSON format
            setLoadedData(response.data);
            setError(null); // Clear any previous errors
        } catch (e) {
            setError(e?.response?.data?.detail || "An error occurred while loading data.");
            setLoadedData(null);
        }
    };

    return (
        <Box display='flex' justifyContent='center' alignItems='center' flexDirection='column' width='100%'>
            <Box display='flex' flexDirection='column' width='100%'>

                {/* Error Display */}
                {error && (
                    <Typography color="error" sx={{ mt: 2 }}>
                        Error: {JSON.stringify(error, null, 2)}
                    </Typography>
                )}

                {/* Load Data Button */}
                <Button
                    onClick={handleLoad}
                    variant="contained"
                    color="primary"
                    disabled={!credentials}
                    sx={{ mt: 2 }}
                >
                    Load Data
                </Button>

                {/* Loaded Data Display */}
                {loadedData && (
                    <Box sx={{ mt: 4 }}>
                        <Typography variant="h6">Fetched Data:</Typography>
                        <TextField
                            fullWidth
                            multiline
                            rows={10}
                            value={JSON.stringify(loadedData, null, 2)} // Pretty-print JSON for readability
                            InputProps={{
                                readOnly: true,
                            }}
                            sx={{ mt: 1 }}
                        />
                    </Box>
                )}

                {/* Clear Data Button */}
                <Button
                    onClick={() => setLoadedData(null)}
                    sx={{ mt: 1 }}
                    variant="contained"
                >
                    Clear Data
                </Button>
            </Box>
        </Box>
    );
};

