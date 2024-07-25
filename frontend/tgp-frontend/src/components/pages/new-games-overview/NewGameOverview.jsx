import {Box, Card, Typography} from "@mui/joy";
import {CardMedia} from "@mui/material";
import React, {useState} from "react";
import {useLoaderData} from "react-router-dom";

function NewGameOverview() {
    const loadedData = useLoaderData();
    const [game] = useState(loadedData.games['results'][5])

    return(
        <>
            <Box sx={{zIndex: -10, left: 0,  position: 'absolute', width: '100%', height: '800px', }}>
                <CardMedia sx={{width: '100%',  marginLeft: 'auto', marginRight: 'auto', filter: 'blur(2px) brightness(35%)', height: '100%', backgroundSize: 'cover',
                    backgroundPositionX: 'center',
                    backgroundPositionY: 'center',
                    mask: 'linear-gradient(180deg, black 58%, rgba(0, 0, 0, 0) 95%), radial-gradient(15.77% 44.22% at 50% 104.95%, rgba(66, 66, 66, 0) 0%, #333333 100%), radial-gradient(30.95% 86.8% at 30.69% 13.2%, rgba(66, 66, 66, 0.33) 0%, #333333 100%), radial-gradient(51.31% 143.89% at 49.99% 24.75%, #000000 0%, #000000 52.6%, rgba(0, 0, 0, 0.18) 83.33%, rgba(0, 0, 0, 0) 95.31%), radial-gradient(51.31% 143.89% at 49.99% 24.75%, #000000 0%, #000000 52.6%, rgba(0, 0, 0, 0.18) 83.33%, rgba(0, 0, 0, 0) 95.31%), linear-gradient(180deg, #000000 90%, rgba(0, 0, 0, 0) 100%)',
                    maskComposite: 'source-in',
                    transition: 'background-image .1s ease-out'
            }} image={"https://images.igdb.com/igdb/image/upload/t_1080p/" + game.screenshot?.image_id + ".webp"}></CardMedia>
        </Box>

            <Box display="flex" sx={{marginTop: '120px !important', width: '100%', height: '334px'}}>
                <CardMedia sx={{minWidth: '250px', minHeight: '100%', backgroundSize: '100%',backgroundPosition: 'center' }} image={"https://images.igdb.com/igdb/image/upload/t_cover_big/" + game.cover?.image_id + ".webp"}></CardMedia>

                <Box
                sx={{padding: '30px', backdropFilter: 'blur(10px)', background: '#00000021', marginLeft: '15px', boxSizing: 'border-box', width: '100%'}}>
                    <Typography sx={{color: 'white'}} level="h1">{game.name}</Typography>
                </Box>
            </Box>
    </>
)

}

export default NewGameOverview;
