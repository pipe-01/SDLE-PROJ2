import { createContext, useEffect, useState } from "react";
import axios from 'axios'

const api = axios.create({
  baseURL: `http://localhost:${process.env.REACT_APP_API_PORT}/`
})

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState();

  useEffect(() => {
    const userToken = localStorage.getItem("user_token");

    if (userToken) setUser({username: JSON.parse(userToken).username});
  }, []);

  const login = async (username, password) => {

    let res = await api.get("/login", { params: { username: username, password: password } })

    if (!res.data.success) {
      return "Failed to Login";
    }
    const token = Math.random().toString(36).substring(2);
    localStorage.setItem("user_token", JSON.stringify({ username, token }));
    setUser({ username });
    return;

  };

  let signup = async (username, password) => {

    let res = await api.get("/register", { params: { username: username, password: password } })

    console.log("res.data = ", res.data)
      console.log("Got here")
      if (!res.data.success) {
        console.log("Got here 2")
        return "There's already an account with this e-mail";
      }
      return;

  };

  const signout = () => {

    api.get("/logout").then(res => {
      console.log("res.data = ", res.data)
      if (!res.data.success) {
        return "Error Logging out";
      }
      setUser(null);
      localStorage.removeItem("user_token");
      return;
    })
  };

  return (
    <AuthContext.Provider
      value={{ user, signed: !!user, login, signup, signout }}
    >
      {children}
    </AuthContext.Provider>
  );
};
