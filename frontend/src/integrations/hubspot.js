import { useState, useEffect } from 'react';
import {
    Box,
    Button,
    CircularProgress,
    List,
    ListItem,
    Typography
} from '@mui/material';
import axios from 'axios';

export const HubSpotIntegration = ({ user, org, integrationParams, setIntegrationParams }) => {
    const [isConnected, setIsConnected] = useState(false);
    const [isConnecting, setIsConnecting] = useState(false);
    const [items, setItems] = useState([]); // Store fetched HubSpot items
    const [error, setError] = useState(null); // Add state for error handling

    // Function to open OAuth in a new window
    const handleConnectClick = async () => {
        try {
            setIsConnecting(true);
            const formData = new FormData();
            formData.append('user_id', user);
            formData.append('org_id', org);

            // Authorize HubSpot
            const response = await axios.post(`http://localhost:8000/integrations/hubspot/authorize`, formData);
            console.log("Authorization URL:", response.data.auth_url);
            const authURL = response.data.auth_url;
            const newWindow = window.open(authURL, 'HubSpot Authorization', 'width=600, height=600');

            // Polling for the window to close
            const pollTimer = window.setInterval(() => {
                if (newWindow?.closed !== false) {
                    window.clearInterval(pollTimer);
                    handleWindowClosed();
                }
            }, 200);
        } catch (e) {
            setIsConnecting(false);
            setError(e?.response?.data?.detail || "Error connecting to HubSpot");
        }
    };

    // Function to handle logic when the OAuth window closes
    const handleWindowClosed = async () => {
        try {
            const formData = new FormData();
            formData.append('user_id', user);
            formData.append('org_id', org);

            // Fetch credentials after OAuth flow
            const response = await axios.post(`http://localhost:8000/integrations/hubspot/credentials`, formData);
            const credentials = response.data;

            if (credentials) {
                setIsConnecting(false);
                setIsConnected(true);
                setIntegrationParams(prev => ({ ...prev, credentials: credentials, type: 'HubSpot' }));

                // Automatically fetch HubSpot items after successful connection
                handleLoadItems();
            }
        } catch (e) {
            setIsConnecting(false);
            setError(e?.response?.data?.detail || "Error fetching HubSpot credentials");
        }
    };

    // Function to load HubSpot items
    const handleLoadItems = async () => {
        try {
            const formData = new FormData();
            formData.append('user_id', user);
            formData.append('org_id', org);

            // Fetch HubSpot items
            const response = await axios.post(`http://localhost:8000/integrations/hubspot/load`, formData);
            console.log("Fetched Items:", response.data.items);
            setItems(response.data.items); // Store fetched items
            setError(null); // Clear any previous errors
        } catch (e) {
            setError(e?.response?.data?.detail || "Error fetching HubSpot items");
        }
    };

    // Update connection status based on existing credentials
    useEffect(() => {
        setIsConnected(integrationParams?.credentials ? true : false);
    }, [integrationParams]);

    return (
        <>
            <Box sx={{ mt: 2 }}>
                <Typography variant="body1">Parameters</Typography>
                <Box display="flex" alignItems="center" justifyContent="center" sx={{ mt: 2 }}>
                    <Button
                        variant="contained"
                        onClick={handleConnectClick}
                        color={isConnected ? 'success' : 'primary'}
                        disabled={isConnecting || isConnected} // Add `disabled` prop
                        aria-label={isConnected ? "HubSpot Connected" : "Connect to HubSpot"} // Add accessibility label
                        style={{
                            pointerEvents: isConnected ? 'none' : 'auto',
                            cursor: isConnected ? 'default' : 'pointer',
                            opacity: isConnected ? 0.7 : 1 // Adjust opacity for disabled state
                        }}
                    >
                        {isConnected ? 'HubSpot Connected' : isConnecting ? <CircularProgress size={20} /> : 'Connect to HubSpot'}
                    </Button>
                </Box>

                {/* Error Display */}
                {error && (
                    <Typography variant="body1" color="error" sx={{ mt: 2 }}>
                        Error: {error}
                    </Typography>
                )}

                {/* Display Fetched Items */}
                {items.length > 0 ? (
                    <Box sx={{ mt: 2 }}>
                        <Typography variant="h6">HubSpot Items:</Typography>
                        <List>
                            {items.map((item) => (
                                <ListItem key={item.id}>
                                    <Typography>
                                        ID: {item.id}, Name: {item.name || "N/A"}, Type: {item.type || "N/A"}
                                    </Typography>
                                </ListItem>
                            ))}
                        </List>
                    </Box>
                ) : (
                    isConnected && (
                        <Typography variant="body1" sx={{ mt: 2 }}>
                            No HubSpot items found.
                        </Typography>
                    )
                )}
            </Box>
        </>
    );
};