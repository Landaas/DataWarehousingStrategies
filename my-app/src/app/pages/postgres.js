'use client'
import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import axios from "axios";
import {
  TextField,
  Stack,
  Button,
  Grid,
} from "@mui/material"

export default function Postgres() {
    const [value, setValue] = React.useState("")
    const [table, setTable] = React.useState([])
    const [headers, setHeaders] = React.useState([]) 
  
    const getData = async (str) => {
      const result = await axios.post("/api/postgresql", str, {headers: {"Content-Type": "application/json"}})
      if (result.status === 200) {
        setHeaders(result.data.headers)
        setTable(result.data.results)
      }
    }
    return ( 
      <Stack spacing={2} display={"flex"} >
        <Button href='http://localhost:8084/'>
          WebUI
        </Button>
        <Grid container flexDirection={"column"} alignItems={"flex-end"} justifyContent={"center"}>
          <Grid container component={Paper} mb={2} width={800}>
            < TextField value={value} onChange={(e) => {e.preventDefault; setValue(e.target.value)}} multiline variant="outlined" fullWidth/>
          </Grid>
          <Grid item display={"flex"} justifyContent={"flex-end"}>
            <Grid item>
              <Button onClick={() => getData(value)} variant="contained">
                Submit
              </Button>
            </Grid>
          </Grid>
        </Grid>
      <Paper>
        <Table>
          <TableHead>
            {headers.map(header => (
              <TableCell>{header}</TableCell>
            ))
            }
          </TableHead>
          <TableBody>
            {table.map((row, index) => (
              <TableRow>
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
    </Stack>
    )
}