import React, { useState } from 'react';
import { SERVER_URL } from '../Constants';
import { useNavigate } from "react-router-dom";
import './PageStyle.css';

function InputPage() {
    const [question, setQuestion] = useState('');
    const [urls, setUrls] = useState(['']);
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const handleInputSubmit = async () => {
        //Input Validation
        if (!question.trim()) {
            setError('Please enter a question.');
            return;
        }
        if (urls.some(url => !url.trim())) {
            setError('Please enter all URLs.');
            return;
        }
        //Submitting data to server
        try {
            const response = await fetch(SERVER_URL + '/submit_question_and_documents', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question, documents: urls }),
            });
            if (response.ok) {
                navigate('/results');
            } else {
                console.error('Failed to submit data');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const handleUrlChange = (e, index) => {
        const newUrls = [...urls];
        newUrls[index] = e.target.value;
        setUrls(newUrls);
    };

    const addUrlInput = () => {
        setUrls([...urls, '']);
    };

    const removeUrlInput = () => {
        if (urls.length > 1) {
            const newUrls = [...urls];
            newUrls.pop();
            setUrls(newUrls);
        }
    };

    return (
        <div className="container">
            <h1 className="title">Call Logs Fact Extractor</h1>
            <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                className="input-field"
                placeholder="Enter your question"
            />
            <br />
            {urls.map((url, index) => (
                <div key={index}>
                    <input
                        type="text"
                        value={url}
                        onChange={(e) => handleUrlChange(e, index)}
                        className="input-field input-field-url"
                        placeholder={`Enter URL ${index+1}`}
                    />
                </div>
            ))}
            {error && <p className="error-message">{error}</p>}
            <button className="url-btn" onClick={addUrlInput}>Add URL</button>
            <button className="url-btn remove-url-btn" onClick={removeUrlInput}>Remove URL</button>
            <br />
            <button className="submit-btn" onClick={handleInputSubmit}>Submit</button>
        </div>
    );
}

export default InputPage;