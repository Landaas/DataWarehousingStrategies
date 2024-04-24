'use-client'
import { createBrowserRouter, useLocation, useNavigate } from 'react-router-dom';
import { Outlet } from 'react-router-dom';
import { Box, Tab, Tabs, Toolbar } from '@mui/material';
import React, { useEffect } from 'react';
import Postgres from './pages/postgres';
import Mongodb from './pages/mongodb';
import Neo from './pages/neo4j';



export default function PageWrapper() {

    const [tab, setTab] = React.useState("postgres")

    const location = useLocation()


    const navigate = useNavigate()

    useEffect(() => {
        setTab(location.pathname.split("/")[1])
      }, [location])

    return (
        <div>
            <Toolbar variant='dense'>
                <Box sx={{ mx: 'auto' }}>
                    <Tabs
                    value={tab == "listings" ? "" : tab}
                    onChange={(e, t) => setTab(t)}
                    aria-label="icon label tabs example"
                    >
                        <Tab value={"postgres"} label="postgres" href='/postgres'/>
                        <Tab value={"mongodb"} label="Mongodb" href='/mongodb'/>
                        <Tab value={"neo4j"} label="neo4j"href='/neo4j' />
                    </Tabs>
                </Box>
            </Toolbar>
            <Box
                sx={{
                my: 4,
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
                }}
            >
                <Outlet/>
            </Box>
        </div>
    )
}

export const router = createBrowserRouter([
    {
      path: '/',
      element: <PageWrapper/>,
      children: [
        {
          path: 'postgres',
          element: <Postgres/>
        },
        {
          path: 'mongodb',
          element: <Mongodb/>
        },
        {
          path: 'neo4j',
          element: <Neo/>
        },
      ]
    },
  ]);