import styled from "styled-components";

export const Container = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
`;

export const UserSection = styled.div`
  display: flex;
  align-items: center;
  padding: 30px;
  flex-direction: column;
  height: 100vh;
  width: 375px;
  gap: 20px;
  background-color: white;
`;

export const UserHeader = styled.div`
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
`;

export const MiddleSection = styled.div`
  display: flex;
  align-items: center;
  padding: 30px;
  flex-direction: column;
  height: 100vh;
  gap: 20px;
`;

export const FollowContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: lightgray;
  width: 305px;
  border-radius: 10px;
  padding: 15px;
`;

export const SmallTitle = styled.h2`
  border-bottom: solid white 1px; 
  text-align: center;
  font-size: 20px;
  width: 100%;
  padding-bottom: 10px;
  margin-bottom: 10px;
`;

export const UserContainer = styled.div`
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 10px;
  border-radius: 10px;
  background-color: white;
  padding: 7px;
  width: 275px;
  margin: 5px;
  padding-right: 12px;
`;

export const FollowSection = styled.div`
  display: flex;
  align-items: center;
  padding: 30px;
  flex-direction: column;
  height: 100vh;
  width: 350px;
  gap: 20px;
  background-color: white;
`;

export const Input = styled.input`
  width: 100%;
  height: 25px;
`;

export const ButtonFollow = styled.button`
  padding: 10px;
  margin-top: 10px;
  outline: none;
  border: none;
  border-radius: 5px;
  width: 60px;
  cursor: pointer;
  background-color: green;
  color: white;
  font-weight: 600;
  font-size: 12px;
`;

export const ButtonUnfollow = styled.button`
  padding: 10px;
  margin-top: 10px;
  outline: none;
  border: none;
  border-radius: 5px;
  width: 70px;
  cursor: pointer;
  background-color: darkred;
  color: white;
  font-weight: 600;
  font-size: 12px;
`;