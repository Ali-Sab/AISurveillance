import Navigation from '../Navigation'
import { Outlet } from 'react-router-dom';

function Layout(props) {
  return <>
    <Navigation />
    <div className="main">
      <Outlet />
    </div>
  </>
}

export default Layout