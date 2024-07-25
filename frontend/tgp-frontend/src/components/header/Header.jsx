import {
    Box,
    List,
    ListItem,
    ListItemButton,
    ListItemDecorator, Select,
    Typography, Option, Autocomplete, Avatar, TextField, styled
} from "@mui/joy";
import React, {useEffect} from "react";
import {Games, Home, Search} from "@mui/icons-material";
import VideogameAssetIcon from '@mui/icons-material/VideogameAsset';
import NewReleasesIcon from '@mui/icons-material/NewReleases';
import {GetAllGames} from "../../axios/BackendService";
import {ListItemAvatar, ListItemText} from "@mui/material";
function Header() {
    const [open, setOpen] = React.useState(false);
    const [gameOptions, setGameOptions] = React.useState([]);
    const [searchValue, setSearchValue] =  React.useState('');

    useEffect(() => {
        if (searchValue) {
            GetAllGames(1, 50, searchValue).then(res => setGameOptions(res.data['results']))
        } else {
            setGameOptions([]);
        }
    }, [searchValue]);


    return (
        <>
            <Box sx={{position: 'absolute',
                left: '0',
                top: '0',
                width: '100%',
                height: '70px',
                background: 'white',
                zIndex: 50,
                borderBottom: '2px solid #0B6BCB'}}>
            </Box>

            <Box sx={{zIndex: 100, height: '70px', color: 'white', justifyContent: 'center', display: 'flex'}}>
                <List
                    role="menuitem"
                    orientation="horizontal"
                    sx={{paddingRight: 0, paddingLeft: 0}}>
                    <ListItem sx={{cursor: 'pointer', padding: "0px"}}>
                        <Box sx={{display: 'flex', flexDirection: 'row', justifyContent: 'center', cursor: 'pointer', padding: "0px", alignItems: 'center'}}>
                            <VideogameAssetIcon fontSize='large' style={{ transform: "rotate(90deg)", color: '#0B6BCB' }}></VideogameAssetIcon>
                            <Typography  sx={{ fontFamily: "Bebas Neue", height: '20px', fontSize: "28px", alignItems: "center", display: "flex", fontWeight: 400, fontStyle: "normal",  textTransform: 'uppercase', color: '#0B6BCB'}}>TGP</Typography>
                        </Box>

                    </ListItem>
                    <ListItem>
                        <List
                            role="menuitemlinks"
                            orientation="horizontal"
                            sx={{paddingRight: 0}}>
                            <ListItem >
                                <ListItemButton
                                    component="a"
                                    href="/">
                                    <ListItemDecorator><Home style={{ color: '' }}/></ListItemDecorator>
                                    <Typography level="body-lg" sx={{color: ''}}>Home</Typography>
                                </ListItemButton>
                                </ListItem>
                            <ListItem>
                                <ListItemButton
                                    component="a"
                                    href="/games">
                                    <ListItemDecorator><Games style={{ color: '' }}/></ListItemDecorator>
                                    <Typography level="body-lg" sx={{color: ''}}>Games</Typography>
                                </ListItemButton>
                            </ListItem>
                            <ListItem>
                                <ListItemButton
                                    component="a"
                                    href="/new-games">
                                    <ListItemDecorator><NewReleasesIcon style={{ color: '' }}/></ListItemDecorator>
                                    <Typography level="body-lg" sx={{whiteSpace: 'nowrap', width: 'fit-content', color: ''}}>New Games</Typography>
                                </ListItemButton>
                            </ListItem>
                        </List>
                    </ListItem>

                    <ListItem sx={{marginLeft: "auto", paddingRight: 0 }}>
                        <Select size="md" ml={5} defaultValue="$">
                            <Option value="$">Dollars ($)</Option>
                            <Option value="£">Pounds (£)</Option>
                        </Select>
                        <Autocomplete
                            startDecorator={<Search />}
                            placeholder="Search all games.."
                            options={gameOptions}
                            onInputChange={(event, newInputValue) => {
                                if (newInputValue.length === 0) {
                                    if (open) setOpen(false);
                                } else {
                                    if (!open) setOpen(true);
                                }
                                setSearchValue(newInputValue);
                            }}
                            noOptionsText="No Games Found"
                            size="md"
                            variant="outlined"
                            color="neutral"
                            getOptionLabel={(option) => option.name || ""}
                            sx={{paddingRight: 0}}
                            renderOption={(props, option) => (
                                <ListItem {...props}>
                                    <ListItemText primary={option.name} secondary={option.summary} />
                                </ListItem>
                            )}
                            open={open}
                            onClose={() => setOpen(false)}
                        />

                    </ListItem>

                </List>
            </Box>
        </>
    );
}

export default Header;
