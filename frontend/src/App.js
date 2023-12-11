import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Live from './components/Live';
import Layout from './components/Layout';
import Archive from './components/Archive';
import Recordings from './components/Recordings';
import NotFound from './components/NotFound';

function App() {
  return (
    <BrowserRouter>
    <Routes>
      <Route path="/" element={ <Layout /> }>
        <Route index element={ <Live /> } />
        <Route path="/live" element={ <Live /> } />
        <Route path="/recordings" element={ <Recordings /> } />
        <Route path="/archive" element={ <Archive /> } />
      </Route>
      <Route path='*' element={<NotFound />}/>
    </Routes>
    </BrowserRouter>
  );
}

export default App;
