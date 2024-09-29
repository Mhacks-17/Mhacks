import axios from 'axios';

const API_URL = "http://35.3.247.253:8000";


export const uploadImage = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await axios.post(`${API_URL}/upload-image/`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data; 
    } catch (error) {
        console.error('Error uploading image:', error);
        throw error; 
    }
};
