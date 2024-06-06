import React, { useState } from 'react';
import axios from 'axios';

const CVUpload = () => {
    const [cv, setCv] = useState(null);
    const [message, setMessage] = useState('');

    const onCVChange = (event) => {
        setCv(event.target.files[0]);
    };

    const onCVUpload = async () => {
        if (!cv) {
            setMessage('No CV selected');
            return;
        }
        const formData = new FormData();
        formData.append('file', cv);

        try {
            const response = await axios.post('http://localhost:5000/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            setMessage(response.data.message);
        } catch (error) {
            setMessage('Error uploading file');
        }
    };

    return (
        <div>
            <h2>CV Upload</h2>
            <input type="file" onChange={onCVChange} />
            <button onClick={onCVUpload}>Upload</button>
            <p>{message}</p>
        </div>
    );
};

export default CVUpload;