// /home/pkimani/getting-started-app/djrssproj-next/components/TopBar.js

import React, { useState } from 'react';
import { AppBar, Toolbar, Typography, IconButton, Menu, MenuItem } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import PaletteIcon from '@mui/icons-material/Palette'; // Icon for color selection
import Link from 'next/link';
import { useTheme } from './themeContext'; // Make sure this path is correct for your project

const TopBar = ({ onMenuClick }) => {
  const { theme, changeTheme } = useTheme(); // Access the theme context
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = (color) => {
    if (color) {
      changeTheme(color);
    }
    setAnchorEl(null);
  };

  // Function to determine the top bar color based on the theme
  const getTopBarColor = () => {
    switch (theme) {
      case 'dark':
        return 'var(--titlebar-bg)';
      case 'pink':
        return 'var(--pink-color)';
      case 'green':
        return 'var(--green-color)';
      case 'yellow':
        return 'var(--yellow-color)';
      case 'purple':
        return 'var(--purple-color)';
      case 'indigo':
        return 'var(--indigo-color)';
      default:
        return 'var(--primary-color)';
    }
  };

  return (
    <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer - 1, backgroundColor: getTopBarColor() }}>
      <Toolbar>
        <IconButton
          edge="start"
          color="inherit"
          aria-label="menu"
          onClick={onMenuClick}
          sx={{ mr: 2 }}
        >
          <MenuIcon />
        </IconButton>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontFamily: 'Bree Serif', color: 'inherit', textAlign: 'center' }}>
          <Link href="/" passHref>
            <a style={{ color: 'inherit', textDecoration: 'none' }}>Articles Plus</a>
          </Link>
        </Typography>
        <IconButton onClick={handleClick} color="inherit">
          <PaletteIcon />
        </IconButton>
        <Menu
          id="theme-menu"
          anchorEl={anchorEl}
          open={open}
          onClose={() => handleClose()}
          MenuListProps={{
            'aria-labelledby': 'theme-button',
          }}
          anchorOrigin={{
            vertical: 'bottom',
            horizontal: 'right',
          }}
          transformOrigin={{
            vertical: 'top',
            horizontal: 'right',
          }}
        >
          <MenuItem onClick={() => handleClose('light')}>Light</MenuItem>
          <MenuItem onClick={() => handleClose('dark')}>Dark</MenuItem>
          <MenuItem onClick={() => handleClose('pink')}>Pink</MenuItem>
          <MenuItem onClick={() => handleClose('green')}>Green</MenuItem>
          <MenuItem onClick={() => handleClose('yellow')}>Yellow</MenuItem>
          <MenuItem onClick={() => handleClose('purple')}>Purple</MenuItem>
          <MenuItem onClick={() => handleClose('indigo')}>Indigo</MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  );
};

export default TopBar;