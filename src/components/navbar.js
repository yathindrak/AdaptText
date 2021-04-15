import React, { useEffect, useState } from "react";
import {
  Navbar,
  NavbarToggler,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink,
  Collapse,
} from "shards-react";
import { useHistory, useLocation  } from 'react-router-dom';
import { login, authFetch, useAuth, logout } from "../auth";

export default function NavigationBar() {
  const [logged] = useAuth();
  const history = useHistory();
  const [collapseOpen, setCollapseOpen] = useState(false);

  const location = useLocation();

  const toggleNavbar = () => {
    setCollapseOpen(!collapseOpen);
  };

  const handleLogout = (e) => {
    e.preventDefault();
    logout()
    history.push('/login')
  }
  return (
    <Navbar type="dark" theme="primary" expand="md">
      <NavbarBrand href="/">AdaptText</NavbarBrand>
      <NavbarToggler onClick={toggleNavbar} />

      <Collapse open={collapseOpen} navbar>
        <Nav navbar className="ml-auto">
          <NavItem>
            <NavLink active={(location.pathname === '/') ? true:false} style={{fontWeight: (location.pathname === '/') ? "500":"400"}} href="/">
              Create
            </NavLink>
          </NavItem>
          <NavItem>
            <NavLink active={(location.pathname === '/tasks') ? true:false} href="/tasks">Tasks</NavLink>
          </NavItem>
          <NavItem>
            <NavLink active={(location.pathname === '/retrain') ? true:false} href="/retrain">Retrain</NavLink>
          </NavItem>
          {logged ? (
            <NavItem>
              <NavLink href="#" onClick={handleLogout}>Log out</NavLink>
            </NavItem>
          ) : null}
        </Nav>
      </Collapse>
    </Navbar>
  );
}
