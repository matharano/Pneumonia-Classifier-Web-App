import colors from '../utils';
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
    backgroundColor: theme.color,
  },
}));

function ProbabilityBar({ probability, color }) {
    return (
        <Box sx={{ width: '100%'}}>
            <BorderLinearProgress variant="determinate" value={probability} theme={{ color: color }} />
        </Box>
    )
}

export default ProbabilityBar;