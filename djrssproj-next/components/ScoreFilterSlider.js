// /home/pkimani/getting-started-app/djrssproj-next/components/ScoreFilterSlider.js

import React, { useState, useEffect } from 'react';
import { Slider, Box, Typography } from '@mui/material';
import axios from 'axios';

const ScoreFilterSlider = ({ queryParams, setQueryParams }) => {
  const [scoreRange, setScoreRange] = useState({ minScore: 0, maxScore: 100 });

  useEffect(() => {
    const fetchScoreRange = async () => {
      try {
        const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}score-range/`);
        const { min_score, max_score } = response.data;
        setScoreRange({
          minScore: min_score,
          maxScore: max_score,
        });
      } catch (error) {
        console.error('Failed to fetch score range:', error);
      }
    };
    fetchScoreRange();
  }, []);

  const handleChange = (event, newValue) => {
    setQueryParams({
      ...queryParams,
      min_score: newValue[0],
      max_score: newValue[1],
    });
  };

  // Generate marks every 5 units
  const generateMarks = (min, max, step) => {
    const marks = [];
    for (let i = min; i <= max; i += step * 2) {
      marks.push({ value: i, label: i.toString() });
    }
    return marks;
  };

  const marks = generateMarks(scoreRange.minScore, scoreRange.maxScore, 5);

  return (
    <Box sx={{ width: '90%', mx: 'auto', my: 2 }}>
      <Typography id="score-range-slider" gutterBottom textAlign="center">
        Score range
      </Typography>
      <Slider
        aria-labelledby="score-range-slider"
        value={[
          queryParams.min_score ? parseInt(queryParams.min_score, 10) : scoreRange.minScore,
          queryParams.max_score ? parseInt(queryParams.max_score, 10) : scoreRange.maxScore,
        ]}
        onChange={handleChange}
        valueLabelDisplay="auto"
        min={scoreRange.minScore}
        max={scoreRange.maxScore}
        step={5}
        marks={marks}
      />
    </Box>
  );
};

export default ScoreFilterSlider;