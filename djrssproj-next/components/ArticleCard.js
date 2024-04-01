// /home/pkimani/getting-started-app/djrssproj-next/components/ArticleCard.js

import React from 'react';
import { Card, CardContent, Typography, Link } from '@mui/material';
import TruncatedText from './TruncatedText';
import Image from 'next/image'; // Import the Next.js Image component

// Custom loader function for the Image component
const customLoader = ({ src }) => {
  return src;
};

const ArticleCard = ({
  article = {
    link: '#',
    image: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/wcAAwAB/aurZ8AAAAAASUVORK5CYII=', 
    title: 'No title',
    author: 'Unknown',
    source: 'Unknown',
    source_url: '#',
    description: 'No description available'
  }
}) => {
  const base64Placeholder = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/wcAAwAB/aurZ8AAAAAASUVORK5CYII=';

  const {
    link,
    image,
    title,
    author,
    source,
    source_url,
    description,
  } = article;

  return (
    <Card className="articleCard" sx={{ maxWidth: 345, backgroundColor: 'var(--background-color)', color: 'var(--text-color)' }}>
      <Link href={link || '#'} target="_blank" rel="noopener noreferrer">
        <div className="imageWrapper">
          <Image
            src={image || base64Placeholder}
            alt={title || 'Article image'}
            layout="fill"
            objectFit="cover"
            loader={customLoader} // Use the custom loader
            onError={(e) => {
              e.target.onerror = null;
              e.target.src = base64Placeholder;
            }}
          />
        </div>
      </Link>
      <CardContent>
        <div className="titleText">
          <Link href={link || '#'} target="_blank" rel="noopener noreferrer">
            <Typography variant="h5" component="div" gutterBottom sx={{ color: 'var(--link-color)' }}>
              {title}
            </Typography>
          </Link>
        </div>
        {author && (
          <Typography variant="body2" color="text.secondary" gutterBottom sx={{ color: 'var(--text-color)' }}>
            By {author}
          </Typography>
        )}
        {source && (
          <div>
            <Link href={source_url || '#'} target="_blank" rel="noopener noreferrer">
              <Typography variant="body2" color="text.secondary" gutterBottom sx={{ color: 'var(--text-color)' }}>
                {source}
              </Typography>
            </Link>
          </div>
        )}
        <div className="descriptionText">
          <TruncatedText text={description || 'No description available'} maxLength={250}/>
        </div>
      </CardContent>
    </Card>
  );
};

export default ArticleCard;