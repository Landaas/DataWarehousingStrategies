
'use-client'
import * as React from 'react';
import Paper from '@mui/material/Paper';
import axios from "axios";
import {
  TextField,
  Stack,
  Button,
  Grid,
} from "@mui/material"


export default function Mongodb() {
    const [value, setValue] = React.useState("")
    const [table, setTable] = React.useState([])
    const [headers, setHeaders] = React.useState([]) 
  
    const getData = async (str) => {
      const result = await axios.post("/api/mongodb", str, {headers: {"Content-Type": "application/json"}})
      if (result.status === 200) {
        setHeaders(result.data.headers)
        setTable(result.data.results)
      }
    }
    return (
        <Stack spacing={2} display={"flex"} >
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
        </Paper>
      </Stack>
    )
}