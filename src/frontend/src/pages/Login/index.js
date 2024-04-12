import React, { useState } from "react";
import Input from "../../components/Input";
import Button from "../../components/Button";
import * as C from "./styles";
import { Link, useNavigate } from "react-router-dom";
import useAuth from "../../hooks/useAuth";

const Login = () => {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [senha, setSenha] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async () => {
    if (!username | !senha) {
      setError("Preencha todos os campos");
      return;
    }

    const res = await login(username, senha);

    if (res) {
      setError(res);
      return;
    }

    navigate("/home");
  };

  return (
    <C.Container>
      <C.Label>Login</C.Label>
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
        <C.labelError>{error}</C.labelError>
        <Button Text="Login" onClick={handleLogin} />
        <C.LabelSignup>
          Doesn't have an account?
          <C.Strong>
            <Link to="/signup">&nbsp;Sign up</Link>
          </C.Strong>
        </C.LabelSignup>
      </C.Content>
    </C.Container>
  );
};

export default Login;
