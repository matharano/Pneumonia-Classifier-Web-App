import './.css';
import React from 'react';
import ImageInput from '../../components/ImageInput';

function Home({setImage}) {
    const inputFileRef = React.useRef();

    const handleImageSelection = (event) => {
        if ( event.target.files && event.target.files[0] ) {
            setImage(event.target.files[0]);
        }
    };

    return (
        <div className='HomePage'>
            <header>
                <h1>Pneumonia Diagnosis</h1>
                <p>Click in the button below to select an image of lungs xray or drop an image to infere whether it presents signs of pneumonia.</p>
                <ImageInput handleChange={handleImageSelection}/>
            </header>
        </div>
    );
};

export default Home;
