// /home/pkimani/getting-started-app/djrssproj-next/components/Sidebar.js

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
import { Checkbox, FormControlLabel, FormGroup, Collapse, Button, Chip } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import axios from 'axios';
import ScoreFilterSlider from './ScoreFilterSlider';
import DateFilterSlider from './DateFilterSlider';

const Sidebar = ({
  isOpen = false,
  toggleSidebar = () => {},
  queryParams
}) => {
  const [sources, setSources] = useState([]);
  const [expanded, setExpanded] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const fetchSources = async () => {
      try {
        const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}sources/`);
        setSources(response.data.sources);
      } catch (error) {
        console.error('Failed to fetch sources:', error);
      }
    };
    fetchSources();
  }, []);

  const handleSortChange = (event, newSort) => {
    if (newSort !== null) {
      router.push({
        pathname: router.pathname,
        query: { ...queryParams, s: newSort },
      }, undefined, { shallow: true });
    }
  };

  const handleItemsChange = (event, newItems) => {
    if (newItems !== null) {
      router.push({
        pathname: router.pathname,
        query: { ...queryParams, i: newItems },
      }, undefined, { shallow: true });
    }
  };

  const handleSourceChange = (newSelectedSources) => {
    router.push({
      pathname: router.pathname,
      query: { ...queryParams, source: newSelectedSources.join(',') },
    }, undefined, { shallow: true });
  };

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  const handleCheckboxChange = (event, source) => {
    const newSelectedSources = event.target.checked
      ? [...queryParams.source?.split(',') || [], source]
      : queryParams.source?.split(',').filter((s) => s !== source) || [];
    handleSourceChange(newSelectedSources);
  };

  const resetFilters = () => {
    router.push({
      pathname: router.pathname,
      query: {}, // Clear all query parameters
    }, undefined, { shallow: true });
  };

  return (
    <Drawer anchor="left" open={isOpen} onClose={toggleSidebar} sx={{ width: '40vw' }} PaperProps={{ sx: { width: '40vw' } }}>
      <List>
        <ListItem>
          <ListItemText primary="Sort Mode" sx={{ textAlign: 'center', width: '100%' }} />
        </ListItem>
        <ListItem>
          <ToggleButtonGroup
            value={queryParams.s || 'date'}
            exclusive
            onChange={handleSortChange}
            aria-label="Sort options"
            fullWidth 
            sx={{ justifyContent: 'center' }}
          >
            <ToggleButton value="date" aria-label="Sort by Date">
              Sort by Date
            </ToggleButton>
            <ToggleButton value="score" aria-label="Sort by Score">
              Sort by Score
            </ToggleButton>
          </ToggleButtonGroup>
        </ListItem>
        <ListItem>
          <ListItemText primary="Articles per Page" sx={{ textAlign: 'center', width: '100%' }} />
        </ListItem>
        <ListItem>
          <ToggleButtonGroup
            value={queryParams.i || '10'} // Default to 10 if not specified
            exclusive
            onChange={handleItemsChange}
            aria-label="Page size options"
            fullWidth
            sx={{ justifyContent: 'center' }}
          >
            <ToggleButton value="10" aria-label="10 items per page">
              10
            </ToggleButton>
            <ToggleButton value="25" aria-label="25 items per page">
              25
            </ToggleButton>
            <ToggleButton value="50" aria-label="50 items per page">
              50
            </ToggleButton>
            <ToggleButton value="75" aria-label="75 items per page">
              75
            </ToggleButton>
            <ToggleButton value="100" aria-label="100 items per page">
              100
            </ToggleButton>
          </ToggleButtonGroup>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton onClick={handleExpandClick} sx={{ justifyContent: 'center', width: '100%' }}>
            <div style={{ visibility: 'hidden' }}>
              {expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
            </div>
            <ListItemText primary="Sources" sx={{ textAlign: 'center', mx: 'auto' }} />
            {expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
          </ListItemButton>
        </ListItem>
        <Collapse in={expanded} timeout="auto" unmountOnExit>
          <FormGroup sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginX: '2vw', maxWidth: '100vw' }}>
            {sources.map((source) => (
              <FormControlLabel
                control={
                  <Checkbox
                    checked={queryParams.source?.split(',').includes(source.source)}
                    onChange={(event) => handleCheckboxChange(event, source.source)}
                  />
                }
                label={source.source}
                key={source.source}
                sx={{width: '100%', margin: '.35rem 0'}}
              />
            ))}
          </FormGroup>
        </Collapse>
        <ScoreFilterSlider
          queryParams={queryParams}
          setQueryParams={(newParams) => router.push({
            pathname: router.pathname,
            query: newParams,
          }, undefined, { shallow: true })}
        />
        <DateFilterSlider
          queryParams={queryParams}
          setQueryParams={(newParams) => router.push({
            pathname: router.pathname,
            query: newParams,
          }, undefined, { shallow: true })}
        />
        <ListItem>
          <Button
            variant="outlined"
            fullWidth
            onClick={resetFilters}
            sx={{ justifyContent: 'center' }}
          >
            Reset Filters
          </Button>
        </ListItem>
      </List>
    </Drawer>
  );
};

export default Sidebar;