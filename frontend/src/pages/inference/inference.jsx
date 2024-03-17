import './.css';
import colors from '../../utils';
import * as React from 'react';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import LinearProgress, { linearProgressClasses } from '@mui/material/LinearProgress';

const BorderLinearProgress = styled(LinearProgress)(({ theme }) => ({
  height: 15,
  borderRadius: 5,
  [`&.${linearProgressClasses.colorPrimary}`]: {
    backgroundColor: colors.white,
  },
  [`& .${linearProgressClasses.bar}`]: {
    borderRadius: 5,
    backgroundColor: colors.blue,
  },
}));

function Inference({image, prediction}) {

    const probability = (100 * prediction['probability']).toFixed(1)
    return(
        <div className='InferencePage' style={{backgroundImage: `url(${URL.createObjectURL(image)})` }} >
            <div className='Background-gradient'>
                <header >
                    <h1>{prediction['prediction'] ? 'Pneumonia detected' : 'Pneumonia undetected'}</h1>
                    <p>{'Pneumonia probability: ' + probability + '%'}</p>
                    <Box sx={{ width: '100%'}}>
                        <BorderLinearProgress variant="determinate" value={probability} />
                    </Box>
                </header>
            </div>
        </div>
    )
};

export default Inference;