// /home/pkimani/getting-started-app/djrssproj-next/components/TruncatedText.js 

import React, { useState } from 'react';
import SanitizedContent from './SanitizedContent';
import truncate from 'html-truncate';
import { Button, Box } from '@mui/material'; // Import the Box component along with Button

const TruncatedText = ({ text, maxLength }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  // Truncated content
  const truncatedContent = isExpanded ? text : truncate(text, maxLength);

  // Determine if the "Show More" button should be displayed
  const shouldShowMoreButton = text.length > maxLength;

  const handleToggle = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <div>
      <SanitizedContent html={truncatedContent} />
      {shouldShowMoreButton && (
        <Box display="flex" justifyContent="center" mt={1}>
          <Button onClick={handleToggle} variant="text" size="small">
            {isExpanded ? 'Show Less' : 'Show More'}
          </Button>
        </Box>
      )}
    </div>
  );
};

export default TruncatedText;