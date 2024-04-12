import styled from "styled-components";

export const Container = styled.div`
  display: flex;
  gap: 15px;
  padding: 20px;

  justify-content: center;
  flex-direction: column;
  gap: 10px;
  max-height: 400px;
  box-shadow: 0 1px 2px #0003;
  background-color: white;
  width: 500px;
  border-radius: 5px;
`;

export const PostHeader = styled.div`
    display: flex;
    align-items: center;
    gap: 15px;
    padding-bottom: 15px;
    border-bottom: solid lightgray 1px;
`;

export const UserUsername = styled.div`
    font-weight: 700;
`;

export const WritePostContent = styled.div`
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 10px;
    margin: 10px;
`;

export const TextAreaPost = styled.textarea`
    width: 100%;
    height: 80px;
    padding: 10px;
`;

export const SubmitButton = styled.button`
    padding: 10px;
    outline: none;
    border: none;
    border-radius: 5px;
    width: 50px;
    cursor: pointer;
    background-color: blue;
    color: white;
    font-weight: 600;
    font-size: 12px;
`;