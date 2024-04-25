
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
import JSONPretty from 'react-json-pretty';
var JSONPrettyMon = require('react-json-pretty/dist/acai');



export default function Mongodb() {
    const [collection, setCollection] = React.useState("")
    const [query, setQuery] = React.useState("")
    const [data, setData] = React.useState()
  
    const getData = async () => {
        if (collection.length) {
            await axios.post("/api/mongodb", JSON.stringify({collection: collection, query: query.length ? query : null}), {headers: {"Content-Type": "application/json"}}).then(res => {
                if (res.status === 200) {
                    setData(res.data)
                }
            }).catch(err => {
                setData(err.message)
            })
        }
    }
    return (
        <Stack spacing={2} display={"flex"} >
          <Button href='http://localhost:8081/'>
            WebUI
          </Button>
          <Grid container flexDirection={"column"} alignItems={"flex-end"} justifyContent={"center"}>
            <Grid container component={Paper} mb={2} width={800}>
                <Stack direction={"row"} display={"flex"} width={"100%"}>
                    <TextField label="Collection" value={collection} onChange={(e) => {e.preventDefault; setCollection(e.target.value)}} multiline variant="outlined" fullWidth/>
                    <TextField label="Query" value={query} onChange={(e) => {e.preventDefault; setQuery(e.target.value)}} multiline variant="outlined" fullWidth></TextField>
                </Stack>
            </Grid>
            <Grid item display={"flex"} justifyContent={"flex-end"}>
              <Grid item>
                <Button onClick={() => getData()} variant="contained">
                  Submit
                </Button>
              </Grid>
            </Grid>
          </Grid>
          {
            data && (
                <Paper>
                    <JSONPretty data={data} theme={JSONPrettyMon}>
    
                    </JSONPretty>
                </Paper>
            )
          }
        </Stack>
    )
}