import React, { useEffect, useState } from 'react';
import { SERVER_URL } from '../Constants';
import './PageStyle.css';

function OutputPage() {
    const [loading, setLoading] = useState(true);
    const [data, setData] = useState(null);
    //Start polling server as the page loads
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(SERVER_URL + '/get_question_and_facts');
                if (response.ok) {
                    const jsonData = await response.json();
                    if (jsonData.status === 'done') {
                        setData(jsonData);
                        setLoading(false);
                    } else {
                        setTimeout(fetchData, 1000); // Polling every 1 second
                    }
                } else {
                    console.error('Failed to fetch data');
                }
            } catch (error) {
                console.error('Error:', error);
            }
        };
        fetchData();
    }, []);

    return (
        <div className="container">
            <h1 className="title">Results</h1>
            {loading ? (
                <div className="loading-animation"></div>
            ) : data ? (
                <div>
                    <h1 className="title-2">Question:</h1>
                    <p>{data.question}</p>
                    <h1 className="title-2">Facts:</h1>
                    {data.facts.length > 0 ? (
                        <ul>
                            {data.facts.map((fact, index) => (
                                <li key={index}>{fact}</li>
                            ))}
                        </ul>
                    ) : (
                        <p>Sorry, no fact found <br />(The provided URLs may be invalid or text files are empty)</p>
                    )}
                </div>
            ) : (
                <p>No data available</p>
            )}
        </div>
    );
}

export default OutputPage;