import './.css';
import React from 'react';

function ErrorPage({ errorDescription }) {

    return (
        <div className='ErrorPage'>
            <header>
                <h1>Error</h1>
                <p>Details: {errorDescription === 'Failed to fetch' ? 'Server is not connected' : errorDescription}</p>
            </header>
        </div>
    );
};

export default ErrorPage;
