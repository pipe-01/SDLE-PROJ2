import { Fragment } from "react";
import { BrowserRouter, Route, Routes, Navigate, Outlet } from "react-router-dom";
import useAuth from "../hooks/useAuth";
import Home from "../pages/Home";
import Login from "../pages/Login";
import Signup from "../pages/Signup";

function AuthenticatedRoute({ element: Element, ...rest }) {
  const { signed } = useAuth();
  
  return signed ? <Outlet /> : <Navigate to="/login" />
}

function NonAuthenticatedRoute({ element: Element, ...rest }) {
  const { signed } = useAuth();
  
  return signed ? <Navigate to="/" /> : <Outlet />
}

const RoutesApp = () => {
  return (
    <BrowserRouter>
      <Fragment>
        <Routes>
          <Route exact path="/" element={<AuthenticatedRoute />} >
            <Route exact path="/" element={<Home />} />
          </Route>
          <Route exact path="/login" element={<NonAuthenticatedRoute />} >
            <Route exact path="/login" element={<Login />} />
          </Route>
          <Route exact path="/signup" element={<NonAuthenticatedRoute />} >
            <Route exact path="/signup" element={<Signup />} />
          </Route>
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </Fragment>
    </BrowserRouter>
  );
};

export default RoutesApp;
