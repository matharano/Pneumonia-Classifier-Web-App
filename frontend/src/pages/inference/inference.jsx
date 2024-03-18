import './.css';
import colors from '../../utils';
import * as React from 'react';
import ProbabilityBar from '../../components/ProbabilityBar';
import ImageInput from '../../components/ImageInput';

function Inference({image, prediction, setImage}) {
    
    var predictionColor = prediction['prediction'] ? colors.red : colors.blue;
    var probability = 100 * prediction['probability'];

    const handleImageSelection = (event) => {
        if ( event.target.files && event.target.files[0] ) {
            setImage(event.target.files[0]);
        }
    };

    return(
        <div className='InferencePage' >
            <h1
                style={{ color: predictionColor }}
            >
                {prediction['prediction'] ? 'Pneumonia detected' : 'Pneumonia undetected'}
            </h1>
            <p>{'Pneumonia probability: ' + probability.toFixed(1) + '%'}</p>
            <ProbabilityBar color={predictionColor} probability={probability} />
            <br/>
            <p className='Disclaimer' >Pneumonia is only declared if probability is higher than 92%.</p>
            <ImageInput title='Upload new image' handleChange={handleImageSelection} />
        </div>
    )
};

export default Inference;