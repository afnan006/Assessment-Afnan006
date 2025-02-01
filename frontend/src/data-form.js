// // import { useState } from 'react';
// // import {
// //     Box,
// //     TextField,
// //     Button,
// // } from '@mui/material';
// // import axios from 'axios';

// // const endpointMapping = {
// //     'Notion': 'notion',
// //     'Airtable': 'airtable',
// //     'HubSpot': 'hubspot',
// // };

// // export const DataForm = ({ integrationType, credentials }) => {
// //     const [loadedData, setLoadedData] = useState(null);
// //     const endpoint = endpointMapping[integrationType];

// //     const handleLoad = async () => {
// //         try {
// //             const formData = new FormData();
// //             formData.append('credentials', JSON.stringify(credentials));
// //             const response = await axios.post(`http://localhost:8000/integrations/${endpoint}/load`, formData);
// //             const data = response.data;
// //             setLoadedData(data);
// //         } catch (e) {
// //             alert(e?.response?.data?.detail);
// //         }
// //     }

// //     return (
// //         <Box display='flex' justifyContent='center' alignItems='center' flexDirection='column' width='100%'>
// //             <Box display='flex' flexDirection='column' width='100%'>
// //                 <TextField
// //                     label="Loaded Data"
// //                     value={loadedData || ''}
// //                     sx={{mt: 2}}
// //                     InputLabelProps={{ shrink: true }}
// //                     disabled
// //                 />
// //                 <Button
// //                     onClick={handleLoad}
// //                     sx={{mt: 2}}
// //                     variant='contained'
// //                 >
// //                     Load Data
// //                 </Button>
// //                 <Button
// //                     onClick={() => setLoadedData(null)}
// //                     sx={{mt: 1}}
// //                     variant='contained'
// //                 >
// //                     Clear Data
// //                 </Button>
// //             </Box>
// //         </Box>
// //     );
// // }

// import { useState } from 'react';
// import {
//     Box,
//     TextField,
//     Button,
//     Typography,
// } from '@mui/material';
// import axios from 'axios';

// const endpointMapping = {
//     'Notion': 'notion',
//     'Airtable': 'airtable',
//     'HubSpot': 'hubspot', // Ensure HubSpot is included
// };

// export const DataForm = ({ integrationType, credentials }) => {
//     const [loadedData, setLoadedData] = useState(null);
//     const [error, setError] = useState(null);

//     const handleLoad = async () => {
//         try {
//             const formData = new FormData();
//             formData.append('credentials', JSON.stringify(credentials));

//             const response = await axios.post(
//                 `http://localhost:8000/integrations/${endpointMapping[integrationType]}/load`,
//                 formData
//             );

//             // Store the fetched data in a readable JSON format
//             setLoadedData(response.data);
//             setError(null); // Clear any previous errors
//         } catch (e) {
//             setError(e?.response?.data?.detail || "An error occurred while loading data.");
//             setLoadedData(null);
//         }
//     };

//     return (
//         <Box display='flex' justifyContent='center' alignItems='center' flexDirection='column' width='100%'>
//             <Box display='flex' flexDirection='column' width='100%'>

//                 {/* Error Display */}
//                 {error && (
//                     <Typography color="error" sx={{ mt: 2 }}>
//                         Error: {error}
//                     </Typography>
//                 )}

//                 {/* Load Data Button */}
//                 <Button
//                     onClick={handleLoad}
//                     variant="contained"
//                     color="primary"
//                     disabled={!credentials}
//                     sx={{ mt: 2 }}
//                 >
//                     Load Data
//                 </Button>

//                 {/* Loaded Data Display */}
//                 {loadedData && (
//                     <Box sx={{ mt: 4 }}>
//                         <Typography variant="h6">Fetched Data:</Typography>
//                         <TextField
//                             fullWidth
//                             multiline
//                             rows={10}
//                             value={JSON.stringify(loadedData, null, 2)} // Pretty-print JSON for readability
//                             InputProps={{
//                                 readOnly: true,
//                             }}
//                             sx={{ mt: 1 }}
//                         />
//                     </Box>
//                 )}

//                 {/* Clear Data Button */}
//                 <Button
//                     onClick={() => setLoadedData(null)}
//                     sx={{ mt: 1 }}
//                     variant="contained"
//                 >
//                     Clear Data
//                 </Button>
//             </Box>
//         </Box>
//     );
// };
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
            formData.append('org_id', 'TestOrg');   // Replace with actual organization ID
    
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

    const renderData = (data) => {
        if (typeof data === 'object' && data !== null) {
            return Object.entries(data).map(([key, value]) => (
                <div key={key}>
                    <strong>{key}:</strong> {JSON.stringify(value, null, 2)}
                </div>
            ));
        }
        return JSON.stringify(data, null, 2); // Pretty-print JSON for readability
    };

    return (
        <Box display='flex' justifyContent='center' alignItems='center' flexDirection='column' width='100%'>
            <Box display='flex' flexDirection='column' width='100%'>

                {/* Error Display */}
                {error && (
                    <Typography color="error" sx={{ mt: 2 }}>
                        Error: {renderData(error)}
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