import Home from "./pages/home/Home";
import Header from "./header/Header";
import {BrowserRouter, createBrowserRouter, Route, RouterProvider, Routes} from "react-router-dom";
import GameOverview from "./pages/game-overview/GameOverview";
import {
    GetAllGameModes, GetAllGamePrices,
    GetAllGames,
    GetAllGenres, GetAllPlatforms,
    GetAllPlayerPerspectives,
    GetAllThemes,
    GetGame
} from "../axios/BackendService";
import GameSearch from "./pages/game-search/GameSearch";
import { CssVarsProvider, extendTheme } from '@mui/joy/styles';
import NewGameOverview from "./pages/new-games-overview/NewGameOverview";


const router = createBrowserRouter([
    {
        path: "/",
        element: <Home />,
        loader: async () => {
            let [topGames, bestDeals, historicallyLow, newlyListed] = await Promise.all([
                GetAllGames(1, 50).then(res => res.data),
            ]);
            return {topGames};
        }
    },
    {
        path: "/games",
        element: <GameSearch />,
        loader: async () => {
            let [games, genres, themes, playerPerspectives, gameModes, platforms] = await Promise.all([
                GetAllGames(1, 50).then(res => res.data),
                GetAllGenres().then(res => res.data),
                GetAllThemes().then(res => res.data),
                GetAllPlayerPerspectives().then(res => res.data),
                GetAllGameModes().then(res => res.data),
                GetAllPlatforms().then(res => res.data),
            ]);
            return {games, genres, themes, playerPerspectives, gameModes, platforms};
        }
    },
    {
        path: "game/:slug",
        element: <GameOverview />,
        loader: async ({params}) => {
            let [game, gamePrices] = await Promise.all([
                GetGame(`${params.slug}`).then(res => res.data),
                GetAllGamePrices(`${params.slug}`, 'en_GB').then(res => res.data),
            ]);
            return {game, gamePrices};
        }
    },
    {
        path: "/new-games",
        element: <NewGameOverview />,
        loader: async ({params}) => {
            let [games] = await Promise.all([
                GetAllGames(1, 10).then(res => res.data),
            ]);
            return {games};
        }
    }
]);

function App() {
  return (
    <div className="app">
        <>
            <Header></Header>
            <RouterProvider router={router} />
        </>
    </div>
  );
}

export default App;
