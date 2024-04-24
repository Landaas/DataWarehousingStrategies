'use client'
import * as React from 'react';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import theme from '@/theme';
import { RouterProvider } from 'react-router-dom';
import { router } from './router';

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
          <ThemeProvider theme={theme}>
            <CssBaseline />
            <RouterProvider router={router}/>
          </ThemeProvider>
      </body>
    </html>
  );
}