import {
    Box,
    Checkbox,
    Chip,
    Dropdown,
    Input,
    MenuItem,
    Typography,
    Menu,
    Card,
    AccordionSummary,
    AccordionDetails, Accordion, AccordionGroup, Grid, FormLabel, MenuButton, CircularProgress
} from "@mui/joy";
import React, {useEffect, useRef, useState} from "react";
import {GameCardSecondary} from "../../misc-cards/GameCardSecondary";
import {useLoaderData} from "react-router-dom";
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import Divider from '@mui/joy/Divider';
import {GetAllGames} from "../../../axios/BackendService";
import {Pagination} from "@mui/material";
import ChipDelete from '@mui/joy/ChipDelete';
import {DeleteForever} from "@mui/icons-material";


function GameSearch() {
    const loadedData = useLoaderData();

    const [hasOneSecondPassed, setHasOneSecondPassed] = useState(false);

    useEffect(() => {
        const timer = setTimeout(() => {
            setHasOneSecondPassed(true);
        }, 1000);
        return () => clearTimeout(timer);
    }, []);


    const [page, setPage] = useState(1)
    const [pageSize, setPageSize] = useState(50)
    const [totalCount, setTotalCount] = useState(loadedData.games['count'])
    const [pageCount, setPageCount] = useState(Math.ceil(loadedData.games['count'] / pageSize))

    const [loadingGameList, setLoadingGameList] = useState(false)
    const [gameListObject, setGameListObject] = useState()
    const [games, setGames] = useState(loadedData.games['results'])
    const [genres] = useState(loadedData.genres)
    const [themes] = useState(loadedData.themes)
    const [playerPerspectives] = useState(loadedData.playerPerspectives)
    const [gameModes] = useState(loadedData.gameModes)
    const [platforms] = useState(loadedData.platforms)
    const [selectedPreset, setSelectedPreset] = React.useState("");

    const [nameSearch, setNameSearch] = useState();
    const [genresSelected, setGenresSelected] = useState();
    const [platformsSelected, setPlatformsSelected] = useState();
    const [gameModesSelected, setGameModesSelected] = useState();
    const [playerPerspectivesSelected, setPlayerPerspectivesSelected] = useState();
    const [themesSelected, setThemesSelected] = useState();
    const [filters, setFilters] = useState([]);


    useEffect(() => {
        if(!hasOneSecondPassed){
            return;
        }
        setLoadingGameList(true)
        GetAllGames(page, pageSize, nameSearch, genresSelected, platformsSelected, gameModesSelected, playerPerspectivesSelected, themesSelected).then(res => setGameListObject(res.data))
    }, [nameSearch, genresSelected, platformsSelected, gameModesSelected, playerPerspectivesSelected, themesSelected, page, pageSize]);

    useEffect(() => {
        if(gameListObject != null){
            setGames(gameListObject['results'])
            setTotalCount(gameListObject['count'])
            setPageCount(Math.ceil(gameListObject['count'] / pageSize))
            setLoadingGameList(false)
        }
    }, [gameListObject]);


    function deleteAllFilters(){
        var array = [...filters];
        filters.forEach((filter)=>{
            array = [...array];
            var index = array.indexOf(filter)
            if (index !== -1) {
                array.splice(index, 1);
            }
        });
        setFilters(array);

    }
    function deleteFilter(filter){
        var array = [...filters];
        var index = array.indexOf(filter)
        if (index !== -1) {
            array.splice(index, 1);
            setFilters(array);
        }
    }

    return (
        <>
            <Box mt={5}>
                <Typography pb={1} level={'h3'}>All Games</Typography>
            </Box>
            <Box mt={2}>
                <Typography pb={1} level={'h4'}>Game Presets</Typography>
                <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
                    {[
                        'Best Deals',
                        'Historically Low',
                        'Popular Games',
                        '> 75% off',
                    ].map((name) => {
                        const checked = selectedPreset === name;
                        return (
                            <Chip
                                key={name}
                                variant="plain"
                                size="lg"
                                color={checked ? 'primary' : 'neutral'}
                            >
                                <Checkbox
                                    variant="outlined"
                                    color={checked ? 'primary' : 'neutral'}
                                    disableIcon
                                    overlay
                                    label={name}
                                    checked={checked}
                                    onChange={(event) => {
                                        setSelectedPreset(name);
                                    }}
                                />
                            </Chip>
                        );
                    })}
                </Box>
            </Box>
            <Box mt={3}>
                <Typography pb={1} level={'h4'}>Filters</Typography>
                <Box sx={{ display: 'flex', gap: 1 }}>
                    <Box>
                        <FormLabel id="select-field-demo-label" htmlFor="select-field-demo-button">
                            Search By Name Or Keywords
                        </FormLabel>
                        <Input onChange={(event) => setNameSearch(event.target.value)} sx={{height: 3}} placeholder="Search Here…" variant="outlined" />
                    </Box>
                    <Box sx={{ display: 'flex', gap: 1}}>
                        <DropdownFilter list={genres} name={'Genre'} setStatusSelected={setGenresSelected} setPage={setPage} filters={filters} setFilters={setFilters}></DropdownFilter>
                    </Box>
                    <Box sx={{ display: 'flex', gap: 1}}>
                        <DropdownFilter list={platforms} name={'Platform'} setStatusSelected={setPlatformsSelected} setPage={setPage} filters={filters} setFilters={setFilters}></DropdownFilter>
                    </Box>
                    <Box sx={{ display: 'flex', gap: 1}}>
                        <DropdownFilter list={playerPerspectives} name={'Player Perspective'} setStatusSelected={setPlayerPerspectivesSelected} setPage={setPage} filters={filters} setFilters={setFilters}></DropdownFilter>
                    </Box>
                    <Box sx={{ display: 'flex', gap: 1}}>
                        <DropdownFilter list={gameModes} name={'Game Mode'} setStatusSelected={setGameModesSelected} setPage={setPage} filters={filters} setFilters={setFilters}></DropdownFilter>
                    </Box>
                    <Box sx={{ display: 'flex', gap: 1}}>
                        <DropdownFilter list={themes} name={'Theme'} setStatusSelected={setThemesSelected} setPage={setPage} filters={filters} setFilters={setFilters}></DropdownFilter>
                    </Box>
                </Box>
            </Box>

            <Box  pt={1} sx={{width: '100%'}}>
                <Divider orientation="horizontal" />
            </Box>
            <Box mt={2} mb={2}>
                {filters.length  > 0 &&
                    <Chip
                        sx={{marginTop: '5px', marginRight: '5px'}}
                        variant="solid"
                        color="danger"
                        size="lg"
                        onClick={() => deleteAllFilters()}
                    >
                        Remove All Filters
                    </Chip>
                }

                {filters.map((filter, index) => (
                    <Chip sx={{marginTop: '5px', marginRight: '5px'}} color="primary" size="lg" key={filter}
                          endDecorator={<ChipDelete onDelete={() => deleteFilter(filter)} />}
                    > {filter}</Chip>
                ))}

            </Box>
            <Box sx={{width: '100%', height: '900px' }}>
                {loadingGameList &&
                    <Box sx={{width: '100%', height: '100%', display: 'flex' }}>
                        <CircularProgress
                            sx={{margin: 'auto'}}
                            color="primary"
                            determinate={false}
                            size="lg"
                            variant="plain"
                        />
                    </Box>

                }
                {!loadingGameList &&
                    <>
                        <Grid container spacing={1}  sx={{ flexGrow: 1}}>
                            {games.slice(0, 22).map((game, index) => (
                                    <Grid key={game.slug}  xs={6}>
                                        <GameCardSecondary game={game}></GameCardSecondary>
                                    </Grid>
                                ))}
                        </Grid>
                            <Typography sx={{textAlign: 'right', marginLeft: 'auto'}} level="body-sm">{totalCount} results</Typography>
                    </>
                }


            </Box>
            <Box pb={10} mt={2}>
                <Pagination size="large" color="primary" count={pageCount} page={page} onChange={(event, value) =>{
                    setPage(value);
                }} />
            </Box>
        </>
    )
}

const DropdownFilter = ({list, name, setStatusSelected, setPage, filters, setFilters}) => {
    const [status, setStatus] = useState(() => {
        const initialState = {};
        list.forEach(state => {
            initialState[state.name] = false;
        });
        return initialState;
    });
    const [open, setOpen] = React.useState(false);

    useEffect(() => {
        setPage(1)
        setStatusSelected(Object.keys(status).filter(key => status[key]));
    }, [status])

    useEffect(() => {
        let newStatusArray = {...status}
        const secondListGenre = filters.map(item => item.split(': ')[1]);

        const filteredScenarios = Object.entries(newStatusArray)
            .filter(([genre, isSelected]) => isSelected && !secondListGenre.includes(genre))
            .map(([genre]) => genre);

        filteredScenarios.forEach(genre => {
            newStatusArray[genre] = false;
        });

        setStatus(newStatusArray)
    }, [filters])

    const handleOpenChange = React.useCallback((event, isOpen) => {
        if(isOpen){
            setOpen(isOpen);
        }
        if(event.type === 'blur' || event.target.tagName == 'BUTTON'){
            setOpen(isOpen)
        }

    }, []);

    function removeFilter(filter){
        var array = [...filters];
        var index = array.indexOf(filter)
        if (index !== -1) {
            array.splice(index, 1);
            setFilters(array);
        }
    }

    function addFilter(filter){
        var array = [...filters];
        array.push(filter)
        setFilters(array)
    }

    return(
        <Box sx={{display: 'flex', alignItems: 'center'}}>
            <Dropdown open={open} onOpenChange={handleOpenChange}>
                <MenuButton sx={{ marginTop: '15px', marginLeft: '15px', padding: '0px'}} size="lg" variant="text" color="primary" endDecorator={<ArrowDropDownIcon />}>{name}</MenuButton>
                <Menu sx={{padding: '10px'}}>
                    <MenuItem sx={{display: 'flex', "&:hover": {backgroundColor: 'inherit !important', color: 'inherit !important'}}}>
                        <Divider style={{width:'100%'}} >
                            {name}
                        </Divider>
                    </MenuItem>
                    <MenuItem sx={{"&:hover": {backgroundColor: 'inherit !important', color: 'inherit !important'}}}>
                        <Grid container spacing={1}  sx={{  flexGrow: 1, width: '400px' }}>
                            {list.slice(0, 12).map((state, index) => (
                                <Grid  key={state.slug}  xs={6}>
                                    <Checkbox key={state.slug} label={state.name} checked={status[state.name]}
                                              onChange={(event) =>{
                                                  setStatus({ ...status, [state.name]: event.target.checked });
                                                  if(event.target.checked ){
                                                      addFilter(name + ": " + [state.name][0])
                                                  }else{
                                                      removeFilter(name + ": " +[state.name][0])
                                                  }
                                              }
                                              }
                                          variant="outlined" />
                                </Grid>
                            ))}
                        </Grid>
                    </MenuItem>
                    <MenuItem sx={{display: 'flex', "&:hover": {backgroundColor: 'inherit !important', color: 'inherit !important'}}}>
                        <Divider style={{width:'100%'}} ></Divider>
                    </MenuItem>
                </Menu>
            </Dropdown>
        </Box>
    )
}
export default GameSearch