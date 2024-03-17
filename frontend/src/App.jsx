import './App.css';
import React from 'react';
import Home from './pages/home/home';
import Inference from './pages/inference/inference';


function App() {
    const [image, setImage] = React.useState();
    const [imageSelected, setImageSelected] = React.useState(false);
    const [inferenceData, setInferenceData] = React.useState(null);

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
        .then(data => {console.log(data); setInferenceData(data)})
    }

    return (
        <div className="App">
            {inferenceData != null ? <Inference image={image} prediction={inferenceData} /> : <Home setImage={handleImageSelection} />}
        </div>
    );
}

export default App;
