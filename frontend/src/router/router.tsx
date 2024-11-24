import { createBrowserRouter } from 'react-router-dom';
import { Suspense } from 'react';
import App from '../App';
import { MainPage } from '../pages/MainPage/MainPage';

export const router = createBrowserRouter([
  {
    path: '/',
    element: (
      <Suspense fallback="">
        <App />
      </Suspense>
    ),
    children: [
      {
        index: true,
        element: <MainPage />,
      },
    ],
  },
]);
