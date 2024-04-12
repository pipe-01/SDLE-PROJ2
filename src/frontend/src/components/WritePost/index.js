import React from "react";
import * as C from "./styles";

const WritePost = ({Username, HandleWritePost}) => {
  return (
    <C.Container>
      <C.PostHeader>
        <img src="user_photo.png" alt="User Photo" width="40" />
        <C.UserUsername>{Username}</C.UserUsername>
      </C.PostHeader>
      <C.WritePostContent>
        <C.TextAreaPost id="write-post" placeholder="Write a Post!"/>
        <C.SubmitButton type="submit" onClick={HandleWritePost} >Post</C.SubmitButton>
      </C.WritePostContent>
    </C.Container>
  );
};

export default WritePost;