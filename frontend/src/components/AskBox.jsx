import React from 'react';

const AskBox = ({ onAsk, loading }) => {
    const [query, setQuery] = React.useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (query.trim()) {
            onAsk(query);
        }
    };

    return (
        <div className="ask-box">
            <h2>Discover Products with AI</h2>
            <form onSubmit={handleSubmit} className="input-group">
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Ask me anything: 'best for gaming', 'work from home'..."
                    disabled={loading}
                />
                <button type="submit" disabled={loading || !query.trim()}>
                    {loading ? 'Searching...' : 'Ask AI'}
                </button>
            </form>
        </div>
    );
};

export default AskBox;
