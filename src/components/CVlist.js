import React, { useState, useEffect } from 'react';
import axios from 'axios';

const CVList = () => {
    const [cvs, setCVs] = useState([]);

    useEffect(() => {
        const fetchCV = async () => {
            try {
                const response = await axios.get('http://localhost:5000/files');
                setCVs(response.data);
            } catch (error) {
                console.error('Error fetching cvs', error);
            }
        };

        fetchCV();
    }, []);

    const deleteCV = async (filename) => {
        try {
            await axios.delete(`http://localhost:5000/files/${filename}`);
            setCVs(cvs.filter(file => file !== filename));
        } catch (error) {
            console.error('Error deleting file', error);
        }
    };

    return (
        <div>
            <h2>Uploaded Files</h2>
            <ul>
                {cvs.map((file, index) => (
                    <li key={index}>
                        <a href={`http://localhost:5000/uploads/${file}`} target="_blank" rel="noopener noreferrer">
                            {file}
                        </a>
                        <button onClick={() => deleteCV(file)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CVList;