import React from 'react';

const ProductCard = ({ product }) => {
    return (
        <div className="card">
            <h3>{product.name}</h3>
            <p style={{ color: '#007bff', fontWeight: 'bold' }}>${product.price}</p>
            <p style={{ fontSize: '0.9rem', color: '#6c757d' }}>{product.category}</p>
            <p style={{ margin: '1rem 0' }}>{product.description}</p>
            <div>
                {product.tags.map(tag => (
                    <span key={tag} className="tag">{tag}</span>
                ))}
            </div>
        </div>
    );
};

export default ProductCard;
