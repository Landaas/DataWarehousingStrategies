/* 'use client'
import Image from "next/image";
import DropdownIframe from "../../DropdownIframe";



export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
        
      <h1>Select an iframe source</h1>
      <DropdownIframe />

    </main>
  );
} */
'use client'
import * as React from 'react';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Link from '@mui/material/Link';
import NextLink from 'next/link';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Papa from "papaparse";
import {
  Toolbar,
  Tabs,
  Tab,
  TextField,
  Stack,
  Button,
  Grid,
} from "@mui/material"
import data from "./dataset.json"
import SyntaxHighlighter from 'react-syntax-highlighter';
import { twilight } from 'react-syntax-highlighter/dist/esm/styles/hljs';


export default function Home() {

  const [tab, setTab] = React.useState("postgres")



  return (
    <Container maxWidth="lg">
      <Toolbar variant='dense'>
        <Box sx={{ mx: 'auto' }}>
          <Tabs
            value={tab == "listings" ? "" : tab}
            onChange={(e, t) => setTab(t)}
            aria-label="icon label tabs example"
          >
            <Tab value={"postgres"} label="Postgres"/>
            <Tab type="secondary" value={"mongo"} label="Mongodb" />
            <Tab type="secondary" value={"neo"} label="neo4j" />
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
        {/* <Stack spacing={2}>
            <Grid container flexDirection={"column"} alignContent={"flex-end"}>
              <Grid container component={Paper} mb={2}>
                < TextField defaultValue="SELECT * FROM battles" multiline variant="outlined" fullWidth/>
              </Grid>
              <Grid item display={"flex"} justifyContent={"flex-end"}>
                <Grid item>
                  <Button variant="contained">
                    Submit
                  </Button>
                </Grid>
              </Grid>
            </Grid>
          <Paper>
            <Table>
              <TableHead>
                <TableCell>bid</TableCell>
                <TableCell>lid</TableCell>
                <TableCell>winner_pid</TableCell>
                <TableCell>loser_pid</TableCell>
                <TableCell>winning_mid</TableCell>
                <TableCell>losing_mid</TableCell>
                <TableCell>duration</TableCell>
                <TableCell>date</TableCell>
              </TableHead>
              <TableBody>
                {data.map((row, index) => (
                  <TableRow>
                    <TableCell>{index}</TableCell>
                    {row.map(cell => (
                      <TableCell>
                        {cell}
                      </TableCell>
                    ))}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </Paper>
        </Stack> */}
        <iframe src='http://127.0.0.1:7474/browser/'/>
      </Box>
    </Container>
  );
}