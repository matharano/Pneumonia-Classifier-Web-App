import './.css';
import colors from '../../utils';
import * as React from 'react';
import ProbabilityBar from '../../components/ProbabilityBar';
import ImageInput from '../../components/ImageInput';

function Inference({image, prediction, setImage}) {
    
    var predictionColor = prediction['prediction'] ? colors.red : colors.blue;
    var probability = (100 * prediction['probability']).toFixed(1)

    const handleImageSelection = (event) => {
        if ( event.target.files && event.target.files[0] ) {
            setImage(event.target.files[0]);
        }
    };

    return(
        <div className='InferencePage' style={{backgroundImage: `url(${URL.createObjectURL(image)})` }} >
            <div className='Background-gradient'>
                <header >
                    <h1
                        style={{ color: predictionColor }}
                    >
                        {prediction['prediction'] ? 'Pneumonia detected' : 'Pneumonia undetected'}
                    </h1>
                    <p>{'Pneumonia probability: ' + probability + '%'}</p>
                    <ProbabilityBar color={predictionColor} probability={probability} />
                    <ImageInput title='Upload new image' handleChange={handleImageSelection} />
                </header>
            </div>
        </div>
    )
};

export default Inference;