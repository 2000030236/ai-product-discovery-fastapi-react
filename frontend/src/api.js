const BASE_URL = 'http://16.171.15.182:8000';

export const fetchProducts = async () => {
    const response = await fetch(`${BASE_URL}/api/products`);
    if (!response.ok) throw new Error('Failed to fetch products');
    return response.json();
};

export const askAI = async (query) => {
    const response = await fetch(`${BASE_URL}/api/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to get AI recommendations');
    }

    return response.json();
};
