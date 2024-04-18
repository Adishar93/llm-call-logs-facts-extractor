import InputPage from './components/InputPage';
import OutputPage from './components/OutputPage';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route exact path="/" element={<InputPage />} />
        <Route path="/results" element={<OutputPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
