import './App.css';
import BackgroundDefault from './media/BackgroundDefault.png';
import React from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import Home from './pages/home/home';
import Inference from './pages/inference/inference';

function AppRoutes() {
    const [image, setImage] = React.useState();
    const [inferenceData, setInferenceData] = React.useState(null);
    const [isLoading, setIsLoading] = React.useState(false);
    const navigate = useNavigate();

    // Redirect user to home page if no data is provided yet
    React.useEffect(() => {
        if (! image && ! inferenceData) {
            navigate('/');
        }
    }, [image, inferenceData, navigate]);

    // Redirect user to home page if no data is provided yet
    const redirectHome = () => {
        setIsLoading(true);
        setImage(null);
        setTimeout(() => {
            navigate('/');
            setIsLoading(false)
        }, 500);
    };

    const handleImageSelection = (imageFile) => {
        // Update image
        setIsLoading(true);

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
            setInferenceData(data);
            setImage(imageFile)
            navigate("/prediction")
            setTimeout(() => setIsLoading(false), 500);
        })
    }

    return (
        <div className="App" style={{ backgroundImage: `url(${image ? URL.createObjectURL(image): BackgroundDefault})` }} >
            <div className='Background-gradient' style={{ animation: isLoading ? 'fadeToBlack 1s forwards' : 'none' }} >
                <a className='NavBar' onClick={redirectHome} >Pneumonia Diagnosis</a>
                <Routes>
                    <Route path="/" element={<Home setImage={handleImageSelection} />} />
                    <Route path="/prediction" element={inferenceData ? <Inference image={image} prediction={inferenceData} setImage={handleImageSelection} /> : null} />
                </Routes>
            </div>
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