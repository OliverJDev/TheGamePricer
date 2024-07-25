import {AspectRatio, Box, Button, Card, CardContent, IconButton, Typography} from "@mui/joy";
import {BookmarkAdd} from "@mui/icons-material";
import React from "react";

export function GameCardPrimary({game}){
    const coverUrl = `https://images.igdb.com/igdb/image/upload/t_cover_big/${game.cover?.image_id}.jpg`;
    return (
        <Card component="a" href={`/game/${game.slug}`} key={game.slug} sx={{"&:hover": {transform: 'scale(1.01)',transition: 'all 0.1s'}, padding: 0, minWidth: '200px', width: '100%', height: '410px'}}>
            <CardContent sx={{padding: '10px', display: 'column', justifyContent: 'space-between'}}>
                <Box height={'50px'}>
                    <Typography level="title-lg"
                                sx={{
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                        display: "-webkit-box",
                        WebkitLineClamp: "2",
                        WebkitBoxOrient: "vertical",
                    }}>{game.name}</Typography>
                </Box>
                <CardContent >
                    <img style={{width: '100%', height: 'auto'}}
                        src={coverUrl}
                    />
                </CardContent>

                <CardContent sx={{marginTop: '5px', alignItems: 'center'}} orientation="horizontal">
                    <div>
                        <Typography level="body-xs">Best price:</Typography>
                        <Typography fontSize="lg" fontWeight="lg">
                            ${game.price?.price}
                        </Typography>
                    </div>

                </CardContent>
            </CardContent>
        </Card>
    );
}

