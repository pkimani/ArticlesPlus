// /home/pkimani/getting-started-app/djrssproj-next/pages/index.js

import React, { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/router';
import { Box, Button, CircularProgress, Alert } from '@mui/material';
import Masonry from '@mui/lab/Masonry';
import ArticleCard from '../components/ArticleCard';
import Sidebar from '../components/Sidebar';
import TopBar from '../components/TopBar';
import axios from 'axios';

// Function to construct the API query string
function constructApiQueryString(params) {
  const query = new URLSearchParams();

  Object.entries(params).forEach(([key, value]) => {
    if (value !== null && value !== undefined && value !== '') {
      query.append(key, value);
    }
  });

  return query.toString();
}

// Function to fetch articles using axios
const fetchArticles = async (queryParams) => {
  const queryString = constructApiQueryString(queryParams);
  try {
    const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}articles/?${queryString}`);
    return response.data;
  } catch (error) {
    throw new Error(error.response ? error.response.data : 'Network response was not ok');
  }
};

const Home = () => {
  const router = useRouter();
  const [articles, setArticles] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [nextCursor, setNextCursor] = useState(null);

  // Store the previous query parameters in a ref
  const queryParams = useRef(router.query);

  // Function to load articles based on current query parameters
  const loadArticles = async (cursor = null) => {
    setIsLoading(true);
    try {
      const data = await fetchArticles({ ...router.query, c: cursor });
      setArticles(cursor ? [...articles, ...data.results] : data.results);
      setNextCursor(data.next_cursor);
    } catch (e) {
      setError(e);
    } finally {
      setIsLoading(false);
    }
  };

  // Effect to fetch articles on initial render and when query parameters change
  useEffect(() => {
    // Function to check if the query parameters have changed
    const haveQueryParamsChanged = (prevQuery, nextQuery) => {
      const prevParams = new URLSearchParams(prevQuery);
      const nextParams = new URLSearchParams(nextQuery);
      for (const [key, value] of prevParams) {
        if (value !== nextParams.get(key)) {
          return true;
        }
      }
      return false;
    };

    // Only fetch articles if the query parameters have changed
    if (haveQueryParamsChanged(queryParams.current, router.query)) {
      setNextCursor(null); // Reset the cursor when filters change
      setArticles([]); // Reset the articles list when filters change
      loadArticles();
    } else if (!queryParams.current || Object.keys(queryParams.current).length === 0) {
      // Fetch articles on initial render if queryParams is empty
      loadArticles();
    }

    // Update the ref when the query parameters change
    queryParams.current = router.query;
  }, [router.query]);

  const handleNextPage = () => {
    if (nextCursor) {
      loadArticles(nextCursor);
    }
  };

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const closeSidebar = () => {
    setSidebarOpen(false);
  };

  if (error) {
    return (
      <Box sx={{ marginTop: '3rem', padding: '1rem' }}>
        <Alert severity="error">{error.message}</Alert>
      </Box>
    );
  }

  return (
    <>
      <TopBar onMenuClick={toggleSidebar} />
      <Sidebar
        isOpen={sidebarOpen}
        toggleSidebar={toggleSidebar}
        queryParams={router.query}
      />
      {sidebarOpen && (
        <div
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            backgroundColor: 'rgba(0, 0, 0, 0.5)',
            zIndex: 1200,
          }}
          onClick={closeSidebar}
        />
      )}
      <Box sx={{ paddingTop: '64px', paddingLeft: '3.5vw', transition: 'margin-left 0.5s', marginLeft: sidebarOpen ? '250px' : '0', marginTop: '20px' }}>
        <Masonry columns={{ xs: 1, sm: 2, md: 3, lg: 4 }} spacing={2}>
          {articles.map((article) => (
            <ArticleCard key={article.hash} article={article} />
          ))}
        </Masonry>
        <Box sx={{ textAlign: 'center', marginY: 4 }}>
          {isLoading ? (
            <CircularProgress />
          ) : (
            nextCursor && (
              <Button variant="contained" onClick={handleNextPage}>
                Load more
              </Button>
            )
          )}
        </Box>
      </Box>
    </>
  );
};

export default Home;