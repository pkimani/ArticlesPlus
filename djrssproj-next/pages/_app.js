// /home/pkimani/getting-started-app/djrssproj-next/pages/_app.js

import { QueryClient, QueryClientProvider, Hydrate } from 'react-query';
import { useState } from 'react';
import { ThemeProvider } from '../components/themeContext'; // Update the path to themeContext.js if necessary
import '../styles/globals.css';

function MyApp({ Component, pageProps }) {
  // Create a client instance with useState to avoid creating a new instance on every render
  const [queryClient] = useState(() => new QueryClient());

  return (
    <QueryClientProvider client={queryClient}>
      <Hydrate state={pageProps.dehydratedState}>
        {/* Wrap the entire application with the ThemeProvider */}
        <ThemeProvider>
          <Component {...pageProps} />
        </ThemeProvider>
      </Hydrate>
    </QueryClientProvider>
  );
}

export default MyApp;