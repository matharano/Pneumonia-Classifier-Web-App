import './App.css';
import React from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import Home from './pages/home/home';
import Inference from './pages/inference/inference';

function AppRoutes() {
    const [image, setImage] = React.useState();
    const [inferenceData, setInferenceData] = React.useState(null);
    const navigate = useNavigate();

    React.useEffect(() => {
        if (! image && ! inferenceData) {
            navigate('/');
        }
    }, [image, inferenceData, navigate]);

    const handleImageSelection = (imageFile) => {
        // Update image
        setImage(imageFile)

        // Send image to backend
        let form = new FormData()
        form.append('file', imageFile )

        fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            mode: "cors",
            body: form
        })
        .then(response => response.json())
        .then(data => {
            console.log(data); 
            setInferenceData(data);
        })
        navigate("/prediction")
    }

    return (
        <div className="App">
            <Routes>
                <Route path="/" element={<Home setImage={handleImageSelection} />} />
                <Route path="/prediction" element={inferenceData ? <Inference image={image} prediction={inferenceData} setImage={handleImageSelection} /> : null} />
            </Routes>
        </div>
    );
}

function App() {
    return (
        <Router>
            <AppRoutes />
        </Router>
    );
}

export default App;