import axios from "axios";

const development = !process.env.NODE_ENV || process.env.NODE_ENV === 'development';

export default function isDev() {
    return development;
}

let backend = ''

if (isDev()) {
    backend = 'http://127.0.0.1:8000/'
}


export const AxiosPublic = axios.create({
    baseURL: backend,
    headers: {
        "Content-Type": "application/json",
    }
});

export function GetGame(slug) {
    return AxiosPublic({
        url: backend + 'games/' + slug,
        method: "GET",
    })
}

export function GetAllGames(page, pageSize, name, genres, platformsSelected, gameModesSelected, playerPerspectivesSelected, themesSelected) {
    const params = {};
    if (name && name.length > 0) params.name = name;
    if (genres && genres.length > 0) params.genres = genres.join(',');
    if (platformsSelected && platformsSelected.length > 0) params.platforms = platformsSelected.join(',');
    if (gameModesSelected && gameModesSelected.length > 0) params.game_modes = gameModesSelected.join(',');
    if (playerPerspectivesSelected && playerPerspectivesSelected.length > 0) params.player_perspectives = playerPerspectivesSelected.join(',');
    if (themesSelected && themesSelected.length > 0) params.themes = themesSelected.join(',');

    params.page_size = pageSize;
    params.page = page;

    return AxiosPublic({
        url: backend + 'games/',
        method: "GET",
        params: params
    })
}

export function GetAllGenres() {
    return AxiosPublic({
        url: backend + 'games/genres/',
        method: "GET",
    })
}

export function GetAllThemes() {
    return AxiosPublic({
        url: backend + 'games/themes/',
        method: "GET",
    })
}
export function GetAllPlatforms() {
    return AxiosPublic({
        url: backend + 'games/platforms/',
        method: "GET",
    })
}

export function GetAllGameModes() {
    return AxiosPublic({
        url: backend + 'games/game-modes/',
        method: "GET",
    })
}

export function GetAllPlayerPerspectives() {
    return AxiosPublic({
        url: backend + 'games/player-perspectives/',
        method: "GET",
    })
}

export function GetAllGamePrices(id, locale) {
    return AxiosPublic({
        url: backend + 'price/get-game-price/' + id + '/' + locale + '/',
        method: "GET",
    })
}