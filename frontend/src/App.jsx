import React, { useState, useEffect } from 'react';
import ProductCard from './components/ProductCard';
import AskBox from './components/AskBox';
import { fetchProducts, askAI } from './api';

function App() {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [askLoading, setAskLoading] = useState(false);
    const [error, setError] = useState(null);
    const [summary, setSummary] = useState('');
    const [results, setResults] = useState([]);

    useEffect(() => {
        loadProducts();
    }, []);

    const loadProducts = async () => {
        try {
            setLoading(true);
            const data = await fetchProducts();
            setProducts(data);
            setError(null);
        } catch (err) {
            setError('Could not load products. Please ensure the backend is running.');
        } finally {
            setLoading(false);
        }
    };

    const handleAsk = async (query) => {
        try {
            setAskLoading(true);
            setError(null);
            const data = await askAI(query);
            setResults(data.products);
            setSummary(data.summary);
        } catch (err) {
            setError(err.message);
        } finally {
            setAskLoading(false);
        }
    };

    return (
        <div className="container">
            <header>
                <h1>DicoVR: AI Product Discovery</h1>
            </header>

            <AskBox onAsk={handleAsk} loading={askLoading} />

            {error && <div className="error-message">{error}</div>}

            {summary && (
                <div className="summary-box">
                    <h3>AI Summary</h3>
                    <p>{summary}</p>
                </div>
            )}

            {results.length > 0 && (
                <section>
                    <h2>Recommended for you</h2>
                    <div className="product-grid">
                        {results.map(product => (
                            <ProductCard key={product.id} product={product} />
                        ))}
                    </div>
                    <hr style={{ margin: '2rem 0', borderColor: '#e9ecef' }} />
                </section>
            )}

            <section>
                <h2>{results.length > 0 ? 'All Products' : 'Product Catalog'}</h2>
                {loading ? (
                    <div className="loading">Loading catalog...</div>
                ) : (
                    <div className="product-grid">
                        {products.map(product => (
                            <ProductCard key={product.id} product={product} />
                        ))}
                    </div>
                )}
            </section>
        </div>
    );
}

export default App;
