import React from "react";
import { useNavigate } from "react-router-dom";
import useAuth from "../hooks/useAuth";

const Root = () => {
  const { signed } = useAuth();
  const navigate = useNavigate();

  signed ? navigate("/home") : navigate("/login");

  return <></>;
};

export default Root;
