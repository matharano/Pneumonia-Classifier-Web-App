import './App.css';
import BackgroundDefault from './media/BackgroundDefault.png';
import React from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import Home from './pages/home/home';
import Inference from './pages/inference/inference';
import ErrorPage from './pages/error/errorPage';
import { quantum } from 'ldrs'
import colors from './utils';

quantum.register()

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
        navigate('/');
        setTimeout(() => setIsLoading(false), 300);
    };

    const handleImageSelection = (imageFile) => {
        // Update image
        setIsLoading(true);
        setTimeout(() => setImage(imageFile), 300);

        // Send image to backend
        let form = new FormData()
        form.append('file', imageFile )
        
        const endpoint = `http://${process.env.REACT_APP_BACKEND_IP}:${process.env.REACT_APP_BACKEND_PORT}/predict`;

        fetch(endpoint, {
            method: "POST",
            mode: "cors",
            body: form
        })
        .then(response =>{
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            } else {
                return response.json()
            }
        })
        .then(data => {
            setInferenceData(data);
            navigate("/prediction");
            setIsLoading(false);
        })
        .catch (error => {
            setInferenceData(error.message);
            navigate('/error');
            setIsLoading(true);
            setTimeout(() => setImage(null), 300);
            setIsLoading(false);
        })
    }

    return (
        <div className="App" style={{ backgroundImage: `url(${image ? URL.createObjectURL(image) : BackgroundDefault})` }} >
            <div className='Background-gradient' style={{ animation: isLoading ? 'fadeToBlack 0.3s forwards' : 'none' }} >
                {isLoading ?
                    <div className='LoadingBanner'>
                        <l-quantum
                            size="150"
                            speed="3" 
                            color={colors.blue} 
                        ></l-quantum>
                    </div>
                    :
                    <>
                        <a className='NavBar' onClick={redirectHome} >Pneumonia Diagnosis</a>
                        <Routes>
                            <Route path="/" element={<Home setImage={handleImageSelection} />} />
                            <Route path="/prediction" element={inferenceData ? <Inference image={image} prediction={inferenceData} setImage={handleImageSelection} /> : null} />
                            <Route path='/error' element={<ErrorPage errorDescription={inferenceData} />} />
                        </Routes>
                    </>
                }
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