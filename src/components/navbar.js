import React, { useEffect, useState } from "react";
import {
  Navbar,
  NavbarToggler,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink,
  Dropdown,
  DropdownToggle,
  DropdownMenu,
  DropdownItem,
  InputGroup,
  InputGroupAddon,
  InputGroupText,
  FormInput,
  Collapse,
} from "shards-react";
import { useHistory } from 'react-router-dom';
import { login, authFetch, useAuth, logout } from "../auth";

export default function NavigationBar() {
  const [logged] = useAuth();
  const history = useHistory();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [collapseOpen, setCollapseOpen] = useState(false);

  const toggleDropdown = () => {
    setDropdownOpen(!dropdownOpen);
  };

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
      <NavbarBrand href="#">AdaptText</NavbarBrand>
      <NavbarToggler onClick={toggleNavbar} />

      <Collapse open={collapseOpen} navbar>
        <Nav navbar className="ml-auto">
          <NavItem>
            <NavLink active href="/">
              Create
            </NavLink>
          </NavItem>
          <NavItem>
            <NavLink href="/tasks">Tasks</NavLink>
          </NavItem>
          {/* <NavItem>
              <NavLink href="#" disabled>
                Disabled
              </NavLink>
            </NavItem> */}
          {logged ? (
            <NavItem>
              <NavLink href="#" onClick={handleLogout}>Log out</NavLink>
            </NavItem>
          ) : null}
          <Dropdown open={dropdownOpen} toggle={toggleDropdown}>
            <DropdownToggle nav caret>
              Dropdown
            </DropdownToggle>
            <DropdownMenu>
              <DropdownItem>Action</DropdownItem>
              <DropdownItem>Another action</DropdownItem>
              <DropdownItem>Something else here</DropdownItem>
            </DropdownMenu>
          </Dropdown>
        </Nav>
      </Collapse>
    </Navbar>
  );
}
