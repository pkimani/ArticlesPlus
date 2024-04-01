// /home/pkimani/getting-started-app/djrssproj-next/components/DateFilterSlider.js

import React, { useState } from 'react';
import { Slider, Box, Typography } from '@mui/material';
import { DateTime } from 'luxon';

const DateFilterSlider = ({ queryParams, setQueryParams }) => {
  // Define the breakpoints for the slider's segments with the new spacing
  const sliderBreakpoints = {
    0: { label: '4 months', subtract: { months: 4 } },
    15: { label: '1 month', subtract: { months: 1 } },
    38: { label: 'This week', subtract: { weeks: 1 } },
    61: { label: 'Today', subtract: { days: 1 } },
    84: { label: 'An hour', subtract: { hours: 1 } },
    100: { label: 'Now', subtract: { hours: 0 } },
  };

  // Function to calculate the date for a given slider value
  const calculateDateForSliderValue = (value) => {
    const now = DateTime.now();
    if (value <= 15) {
      return now.minus(sliderBreakpoints[0].subtract).startOf('day');
    } else if (value <= 38) {
      return now.minus(sliderBreakpoints[15].subtract).startOf('day');
    } else if (value <= 61) {
      return now.minus(sliderBreakpoints[38].subtract).startOf('day');
    } else if (value <= 84) {
      return now.minus(sliderBreakpoints[61].subtract).startOf('day');
    } else if (value <= 100) {
      return now.minus(sliderBreakpoints[84].subtract).startOf('day');
    }
  };

  // Create marks based on the breakpoints with the oldest applicable date
  const sliderMarks = Object.entries(sliderBreakpoints).map(([value, { label }]) => ({
    value: parseInt(value),
    label,
  }));

  // Initial slider value (0% by default, which corresponds to 4 months ago)
  const [sliderValue, setSliderValue] = useState(0);

  // Function to handle slider value change
  const handleSliderChange = (event, newValue) => {
    setSliderValue(newValue);
    const date = calculateDateForSliderValue(newValue);
    setQueryParams({
      ...queryParams,
      start_date: date.toISODate(),
    });
  };

  // Function to format the value label to display the calendar date in local format
  const valueLabelFormat = (value) => {
    const date = calculateDateForSliderValue(value);
    return date.toFormat('MM/dd/yy'); // Format the date as MM/dd/yy
  };

  return (
    <Box sx={{ width: '90%', mx: 'auto', my: 2 }}>
      <Typography id="date-range-slider" gutterBottom textAlign="center">
        Date range
      </Typography>
      <Slider
        aria-labelledby="date-range-slider"
        value={sliderValue}
        onChange={handleSliderChange}
        valueLabelDisplay="on"
        step={null} // Set step to null to snap to marks
        marks={sliderMarks}
        min={0}
        max={100}
        valueLabelFormat={valueLabelFormat}
      />
    </Box>
  );
};

export default DateFilterSlider;