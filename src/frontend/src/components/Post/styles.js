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

export const UserPhoto = styled.img`
`;

export const UserUsername = styled.div`
    font-weight: 700;
`;

export const PostTime = styled.div`
    margin-left: auto;
`;

export const PostContent = styled.div`
    margin: 10px;
`;
