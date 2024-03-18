import React from 'react';
import colors from '../utils';
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

function ImageInput({ title='Upload image', handleChange }) {
    const inputFileRef = React.useRef();

    return (
        <>
            <ColorButton
                variant='outlined'
                size='large'
                endIcon={<UploadRoundedIcon />}
                onClick={() => inputFileRef.current.click()}
            >
                {title}
            </ColorButton>
            <input
                className="Upload-button"
                type="file"
                accept=".jpg,.jpeg,.png"
                ref={inputFileRef}
                onChange={handleChange}
                hidden 
            />
        </>
    );
}

export default ImageInput;
