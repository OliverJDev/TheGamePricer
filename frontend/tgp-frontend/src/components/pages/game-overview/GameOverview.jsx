import {Box, Button, ButtonGroup, Card, Chip, Grid, Stack, Typography} from "@mui/joy";
import {CardMedia} from "@mui/material";
import {useLoaderData, useNavigate} from "react-router-dom";
import React, {useEffect, useRef, useState} from "react";
import {FavoriteBorder, KeyboardArrowRight} from "@mui/icons-material";
import Table from '@mui/joy/Table';
import LocalOfferOutlinedIcon from '@mui/icons-material/LocalOfferOutlined';
import windows from "../../../images/windows.png";
import Sheet from '@mui/joy/Sheet';

function GameOverview() {
    const loadedData = useLoaderData();
    const [game] = useState(loadedData.game)
    const [gamePrices] = useState(loadedData.gamePrices['results'])


    function getGenres() {
        return game.genres.map((item, index) => (
            <span key={index}>
                <a href={`/genres/${item.slug}`}>
                    {item.name}
                </a>
                {index < game.genres.length - 1 && ', '}
            </span>
        ));
    }

    function getPlatforms() {
        return game.platforms.map((item, index) => (
            <span key={index}>
                <a href={`/platforms/${item.slug}`}>
                    {item.name}
                </a>
                {index < game.platforms.length - 1 && ', '}
            </span>
        ));
    }
    function formatDate(inputDateString) {
        const date = new Date(inputDateString);
        const options = { day: '2-digit', month: 'short', year: 'numeric' };
        return new Intl.DateTimeFormat('en-GB', options).format(date);
    }

    return (
        <Stack
            direction="column"
            spacing={2}
        >
            <Box sx={{zIndex: -10,  position: 'absolute', top: '50px', left: '0px', width: '100%', height: '500px', }}>
                <CardMedia sx={{width: '100%',  filter: ' brightness(25%)', height: '100%', backgroundSize: '100%'
                }} image={"https://images.igdb.com/igdb/image/upload/t_1080p/" + game.screenshot?.image_id + ".webp"}></CardMedia>
                <Box sx={{ zIndex: 100, position: 'relative', top: '-13px', left: '0', background: '#efefef'}}>'</Box>
            </Box>



            <Box display="flex" sx={{marginTop: '200px !important', width: '100%', height: '525px'}}>
                <CardMedia sx={{minWidth: '375px', minHeight: '100%', backgroundSize: '100%',backgroundPosition: 'top' }} image={"https://images.igdb.com/igdb/image/upload/t_cover_big/" + game.cover?.image_id + ".webp"}></CardMedia>
                <Box ml={'30px'} sx={{height: '500px', display: 'flex', flexDirection: 'column'}}>
                    <Box sx={{minHeight: '265px', maxHeight: '265px', display: 'flex', flexDirection: 'column'}}>
                        <Typography sx={{color: 'white'}} level="h1">{game.name}</Typography>
                        <Typography level={'body-lg'}
                            sx={{
                                color: 'white',
                                overflow: 'hidden',
                                textOverflow: 'ellipsis',
                                display: '-webkit-box',
                                WebkitLineClamp: '4',
                                WebkitBoxOrient: 'vertical',
                                lineHeight: '22px',
                            }}
                        >{game.summary}
                        </Typography>
                        <Box sx={{marginTop: 'auto', marginBottom: 'auto', paddingBottom: '10px'}}>
                            <Typography sx={{color: 'white'}} level="body-lg">Genres: {getGenres()}</Typography>
                            <Typography sx={{color: 'white'}} level="body-lg">Platforms: {getPlatforms()}</Typography>
                        </Box>
                    </Box>
                    <Box mt={'15px'} sx={{height: '100%', width: '100%'}}>
                        <Card sx={{display: 'flex', boxSizing: 'border-box', height: '100%', width: '100%', overflow: 'hidden'}}>
                            <Grid container spacing={2} sx={{ flexGrow: 1}}>
                                <Grid sx={{maxHeight: '95px'}} xs={3}>
                                    <Typography mb={'3px'} level={"body-sm"}>Release Date</Typography>
                                    <Chip mt={'3px'} style={{overflow: "hidden", textOverflow: "ellipsis", maxWidth:'150px'}}>{formatDate(game.first_release_date)}</Chip>
                                </Grid>
                                <Grid sx={{maxHeight: '95px'}} xs={3}>
                                    <Typography mb={'3px'} level={"body-sm"}>Theme</Typography>
                                    {game.themes.map((theme) => (
                                        <Chip key={theme.slug} mt={'3px'} style={{overflow: "hidden", textOverflow: "ellipsis", maxWidth:'150px'}}>{theme.name}</Chip>
                                    ))}
                                    {game.themes.length === 0 && <Chip key={'empty-themes'}>Not Specified</Chip>}

                                </Grid>

                                <Grid sx={{display: 'flex', alignItems: 'center', justifyContent: 'space-between',maxHeight: '95px'}} xs={6}>
                                    <Button sx={{width: '175px' }}variant={'soft'}
                                            startDecorator={<FavoriteBorder />}>
                                        Add To Collection
                                    </Button>
                                    <Button sx={{width: '175px' }}variant={'soft'}
                                            startDecorator={<LocalOfferOutlinedIcon />}>
                                        Create Price Alert
                                    </Button>
                                </Grid>
                            </Grid>
                            <Grid container spacing={2} sx={{ flexGrow: 1 }}>
                                <Grid sx={{maxHeight: '95px'}} xs={3}>
                                    <Typography mb={'3px'} level={"body-sm"}>Game Engine</Typography>
                                    {game.game_engines.map((game_engine) => (
                                        <Chip key={game_engine.slug} mt={'3px'} style={{overflow: "hidden", textOverflow: "ellipsis", maxWidth:'150px'}}>{game_engine.name}</Chip>
                                    ))}
                                    {game.game_engines.length === 0 && <Chip key={'empty-game_engines'}>Not Specified</Chip>}

                                </Grid>
                                <Grid sx={{maxHeight: '95px'}} xs={3}>
                                    <Typography mb={'3px'} level={"body-sm"}>Game Mode</Typography>
                                    {game.game_modes.map((game_mode) => (
                                        <Chip key={game_mode.slug} mt={'3px'} style={{overflow: "hidden", textOverflow: "ellipsis", maxWidth:'150px'}}>{game_mode.name}</Chip>
                                    ))}
                                    {game.game_modes.length === 0 && <Chip key={'empty-game_mode'}>Not Specified</Chip>}

                                </Grid>
                                <Grid sx={{maxHeight: '95px'}} xs={3}>
                                    <Typography mb={'3px'} level={"body-sm"}>Player Perspective</Typography>
                                    {game.player_perspectives.map((player_perspective) => (
                                        <Chip key={player_perspective.slug} mt={'3px'} style={{overflow: "hidden", textOverflow: "ellipsis", maxWidth:'150px'}}>{player_perspective.name}</Chip>
                                    ))}
                                    {game.player_perspectives.length === 0 && <Chip key={'empty-player_perspectives'}>Not Specified</Chip>}
                                </Grid>
                                <Grid sx={{maxHeight: '95px'}} xs={3}>
                                    <Typography mb={'3px'} level={"body-sm"}>Involved Company</Typography>
                                    {game.companies.map((company) => (
                                        <Chip key={company.slug} mt={'3px'} style={{overflow: "hidden", textOverflow: "ellipsis", maxWidth:'150px'}}>{company.name}</Chip>
                                    ))}
                                    {game.companies.length === 0 && <Chip key={'empty-companies'}>Not Specified</Chip>}
                                    </Grid>
                            </Grid>
                        </Card>
                    </Box>
                </Box>

            </Box>
            <Box pt={3}>
                <Typography pb={1} level={'title-lg'}>Game Price Comparison Table</Typography>
                <GamePriceTable gamePrices={gamePrices}></GamePriceTable>
            </Box>
            <Box pt={3}>
                <Typography pb={1} level={'title-lg'}>Games Similar To {game.name}</Typography>
                <Box>
                    <Grid container spacing={1} sx={{ flexGrow: 1 }}>
                        <Grid container spacing={1} sx={{ flexGrow: 1 }}>

                        </Grid>
                    </Grid>
                </Box>
            </Box>
        </Stack>
    );
}


function GamePriceTable(gamePrices){
    gamePrices = gamePrices['gamePrices']
    
    return (
        <Sheet variant="solid"
               color="primary"
               sx={{ p: 2, borderRadius: 'sm' }}>
            <Table variant="solid"
                   color="primary">
                <thead>
                <tr>
                    <th style={{ width: '40%',color: 'white', borderColor: 'white' }}>Store</th>
                    <th style={{ color: 'white', borderColor: 'white' }}>Platforms</th>
                    <th style={{ color: 'white', borderColor: 'white' }}>Price</th>
                    <th style={{ color: 'white', borderColor: 'white' }}></th>
                </tr>
                </thead>
                <tbody>
                {gamePrices.map((gamePrice, index) => (
                    <>
                        <tr>
                            <td>
                                <img style={{'width': '175px', 'filter': 'brightness(0) invert(1)'}} src={require(`../../../images/store-logos/${gamePrice.store.name.toLowerCase().replace(/ /g, '_')}.png`)}></img>
                            </td>
                            <td>
                                <img style={{'width': '25px', 'filter': 'brightness(0) invert(1)'}} src={windows}></img>
                            </td>
                            <td><Typography color={'white'} level={'body-lg'} fontWeight="lg">£{gamePrice.price}</Typography></td>
                            <td>
                                <Button
                                    component="a"
                                    href={gamePrice.url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    sx={{color: 'white', border: 'white 1px solid'}}
                                    endDecorator={<KeyboardArrowRight />}>
                                    Buy Now

                                </Button>
                            </td>
                        </tr>
                    </>
                ))}
                </tbody>

            </Table>
        </Sheet>

    );
}
export default GameOverview;
