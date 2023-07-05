import React from 'react'
import ReactDOM from 'react-dom/client'
import {BrowserRouter, Routes, Route} from 'react-router-dom'

import './index.css'

import Layout from "./pages/layout/Layout";
import Home from "./pages/home/Home"
import ChecklistList from "./pages/checklistList/ChecklistList";
import {MantineProvider} from "@mantine/core";

export default function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Layout/>}>
                    <Route index element={<Home/>}/>
                    <Route path="/checklist" element={<ChecklistList/>}/>
                </Route>
            </Routes>
        </BrowserRouter>
    );
}


ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
    <React.StrictMode>
        <MantineProvider>
            <App/>
        </MantineProvider>
    </React.StrictMode>
);
