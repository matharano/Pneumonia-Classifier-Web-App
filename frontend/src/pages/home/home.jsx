import './home.css';
import React from 'react';
import colors from '../../utils';
import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';
import UploadRoundedIcon from '@mui/icons-material/UploadRounded';

const ColorButton = styled(Button)(({ theme }) => ({
    color: colors.blue,
    '&:hover': {
      backgroundColor: colors.blue,
      color: theme.palette.getContrastText(colors.blue)
    },
  }));

function Home({setImage}) {
    const inputFileRef = React.useRef();

    const handleImageSelection = (event) => {
        if ( event.target.files && event.target.files[0] ) {
            setImage(event.target.files[0]);
        }
    };

    return (
        <div className='Page'>
            <header>
                <h1>Pneumonia diagnosis</h1>
                <p>Click in the button below to select an image of lungs xray or drop an image to infere whether it presents signs of pneumonia.</p>
                <ColorButton
                    variant='outlined'
                    size='large'
                    endIcon={<UploadRoundedIcon />}
                    onClick={() => inputFileRef.current.click()}
                >
                    Upload image
                </ColorButton>
                <input
                    className="Upload-button"
                    type="file"
                    accept=".jpg,.jpeg,.png"
                    ref={inputFileRef}
                    onChange={handleImageSelection}
                    hidden />
            </header>
        </div>
    );
}

export default Home;
