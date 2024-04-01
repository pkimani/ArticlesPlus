// /home/pkimani/getting-started-app/djrssproj-next/components/SanitizedContent.js

import React from 'react';
import DOMPurify from 'isomorphic-dompurify';

const SanitizedContent = ({ html }) => {
  const sanitizedHTML = DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['p', 'div', 'section', 'article', 'a'],
    ALLOWED_ATTR: ['href', 'target', 'rel'],
  });

  return <div dangerouslySetInnerHTML={{ __html: sanitizedHTML }} />;
};

export default SanitizedContent;