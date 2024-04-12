import React, { useState } from "react";
import Input from "../../components/Input";
import Button from "../../components/Button";
import * as C from "./styles";
import { Link, useNavigate } from "react-router-dom";
import useAuth from "../../hooks/useAuth";

const Signup = () => {
  const [username, setUsername] = useState("");
  const [senha, setSenha] = useState("");
  const [senhaConf, setSenhaConf] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const { signup } = useAuth();

  const handleSignup = async () => {
    if (!username | !senha | !senhaConf) {
      setError("Missing Information");
      return;
    } else if (senha !== senhaConf) {
      setError("The passwords are not the same");
      return;
    }

    let res = await signup(username, senha);

    if (res) {
      setError(res);
      return;
    }

    alert("Successfully Registered User");
    navigate("/");
  };

  return (
    <C.Container>
      <C.Label>Sign up</C.Label>
      <C.Content>
        <Input
          type="username"
          placeholder="Username"
          value={username}
          onChange={(e) => [setUsername(e.target.value), setError("")]}
        />
        <Input
          type="password"
          placeholder="Password"
          value={senha}
          onChange={(e) => [setSenha(e.target.value), setError("")]}
        />
        <Input
          type="password"
          placeholder="Password Confirmation"
          value={senhaConf}
          onChange={(e) => [setSenhaConf(e.target.value), setError("")]}
        />
        <C.labelError>{error}</C.labelError>
        <Button Text="Sign up" onClick={handleSignup} />
        <C.LabelSignin>
          Already have an account?
          <C.Strong>
            <Link to="/">&nbsp;Login</Link>
          </C.Strong>
        </C.LabelSignin>
      </C.Content>
    </C.Container>
  );
};

export default Signup;
