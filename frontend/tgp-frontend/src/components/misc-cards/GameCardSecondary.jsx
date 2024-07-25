import {Box, Button, Card, CardOverflow, styled, Typography} from "@mui/joy";
import React from "react";
import Tippy from '@tippyjs/react';
import {followCursor} from 'tippy.js';


export function GameCardSecondary({game}){
    let coverUrl;
    if (game.header){
        coverUrl = `https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/${game.header.image_id}/header.jpg`;
    }else{
        coverUrl = `https://images.igdb.com/igdb/image/upload/t_screenshot_big/${game.artwork?.image_id}.jpg`;
    }

    return (
        <>
            <Card component="a" href={`/game/${game.slug}`} orientation="horizontal" sx={{"&:hover": {transform: 'scale(1.01)',transition: 'all 0.1s'}, padding: 0, width: '100%', height: '70px', overflow: 'hidden'}}>
                <CardOverflow sx={{height: '100%'}}>
                    <img style={{width: '175px'}}
                        src={coverUrl}
                    />
                </CardOverflow>
                <CardOverflow sx={{padding: '5px', pl: 0, display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', width: '100%'}}>
                    <Typography level="title-md"
                                sx={{
                                    fontWeight: 600,
                                    overflow: "hidden",
                                    textOverflow: "ellipsis",
                                    display: "-webkit-box",
                                    WebkitLineClamp: "1",
                                    WebkitBoxOrient: "vertical",
                                }}>{game.name}</Typography>
                    <Box>
                        <Typography level="body-xs">Best Price:</Typography>
                        <Typography fontWeight="md">
                            $10.29
                        </Typography>
                    </Box>
                </CardOverflow>
            </Card>
        </>

    );
}
