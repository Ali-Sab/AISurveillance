import Navbar from 'react-bootstrap/Navbar';
import Container from 'react-bootstrap/Container';
import NavbarBrand from 'react-bootstrap/esm/NavbarBrand';
import LinkContainer from 'react-router-bootstrap/LinkContainer';
import Nav from 'react-bootstrap/Nav';
import { NavLink } from 'react-router-dom';

function Navigation(props) {
    return <div>
        <Navbar>
            <Container fluid>
                <LinkContainer to="/">
                    <NavbarBrand>AISurveillance</NavbarBrand>
                </LinkContainer>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse>
                    <Nav className="me-auto">
                        <Nav.Item><NavLink className="nav-link" to={"/live"}>Live</NavLink></Nav.Item>
                        <Nav.Item><NavLink className="nav-link" to={"/recordings"}>Recordings</NavLink></Nav.Item>
                        <Nav.Item><NavLink className="nav-link" to={"/archive"}>Archive</NavLink></Nav.Item>
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    </div>
}

export default Navigation