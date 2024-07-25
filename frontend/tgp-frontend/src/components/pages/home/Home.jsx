import {AspectRatio, Box, Button, Card, CardContent, CardOverflow, Grid, IconButton, Stack, Typography} from "@mui/joy";
import React, {useState} from "react";
import {BookmarkAdd, KeyboardArrowRight} from "@mui/icons-material";
import KeyboardDoubleArrowRightIcon from '@mui/icons-material/KeyboardDoubleArrowRight';
import { CardMedia } from '@mui/material';
import {GameCardPrimary} from "../../misc-cards/GameCardPrimary";
import {GameCardSecondary} from "../../misc-cards/GameCardSecondary";
import {useLoaderData} from "react-router-dom";

function Home() {
    const loadedData = useLoaderData();
    const [topGames] = useState(loadedData.topGames['results'])

    return (
        <Stack
            direction="column"
            justifyContent="center"
            alignItems="center"
            spacing={2}
        >

            <CardMedia sx={{ opacity: '0.025', backgroundSize: '20%', position: 'absolute',backgroundRepeat: 'repeat', top: 70, left: 0, width: '100%', height: '100vw'}} image={"https://img.freepik.com/premium-vector/black-white-background-pattern-pixel-art-style_475147-2981.jpg"}></CardMedia>

            <Box sx={{width: '100%'}}>
                <Typography level="title-lg" sx={{marginBottom: '15px'}}>Top Games</Typography>
                <Grid container spacing={1} sx={{ flexGrow: 1 }}>
                    {topGames.slice(0, 10).map((game, index) => (
                        <Grid key={game.slug} xs={2.4}><GameCardPrimary game={game}/></Grid>
                    ))}
                </Grid>
            </Box>
            <Box display={"flex"} flexDirection={'column'} sx={{width: '100%'}}>
                <Typography  mb={'10px'} level="title-lg">Best Deals</Typography>

                <Grid container spacing={0.5}  sx={{ flexGrow: 1 }}>
                    {topGames.slice(0, 12).map((game, index) => (
                        <Grid  key={game.slug} xs={6}>
                            <GameCardSecondary game={game}></GameCardSecondary>
                        </Grid>
                    ))}
                </Grid>
                <Button sx={{marginTop: '10px', width: 'fit-content',marginLeft: 'auto'}} endDecorator={<KeyboardDoubleArrowRightIcon  />} variant="solid">
                    View More
                </Button>
            </Box>

            <Box display={"flex"} flexDirection={'column'} sx={{width: '100%'}}>
                <Typography  mb={'10px'}level="title-lg">Newly Listed</Typography>

                <Grid container spacing={0.5}  sx={{ flexGrow: 1 }}>
                    {topGames.slice(0, 12).map((game, index) => (
                        <Grid key={game.slug}   xs={6}>
                            <GameCardSecondary  game={game}></GameCardSecondary>
                        </Grid>
                    ))}
                </Grid>
                <Button sx={{marginTop: '10px', width: 'fit-content',marginLeft: 'auto'}} endDecorator={<KeyboardDoubleArrowRightIcon  />} variant="solid">
                    View More
                </Button>
            </Box>
            <Box display={"flex"} flexDirection={'column'} sx={{width: '100%'}}>
                <Typography  mb={'10px'} level="title-lg">Historically Low</Typography>
                <Grid container spacing={0.5}  sx={{ flexGrow: 1 }}>
                    {topGames.slice(0, 12).map((game, index) => (
                        <Grid  key={game.slug}  xs={6}>
                            <GameCardSecondary  game={game}></GameCardSecondary>
                        </Grid>
                    ))}
                </Grid>
                <Button sx={{marginTop: '10px', width: 'fit-content',marginLeft: 'auto'}} endDecorator={<KeyboardDoubleArrowRightIcon  />} variant="solid">
                    View More
                </Button>
            </Box>
        </Stack>
    )
}

export default Home;
