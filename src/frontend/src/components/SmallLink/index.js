import React from "react";
import * as C from "./styles";

const SmallLink = ({ Text, onClick, Type = "button" }) => {
  return (
    <C.SmallLink type={Type} onClick={onClick}>
      {Text}
    </C.SmallLink>
  );
};

export default SmallLink;
