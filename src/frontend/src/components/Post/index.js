import React from "react";
import * as C from "./styles";

const Post = ({ Username, Time, Content }) => {
  return (
    <C.Container>
      <C.PostHeader>
        <C.UserPhoto src="user_photo.png" alt="User Photo" width="40" />
        <C.UserUsername>{Username}</C.UserUsername>
        <C.PostTime>{Time}</C.PostTime>
      </C.PostHeader>
      <C.PostContent>
        {Content}
      </C.PostContent>
    </C.Container>
  );
};

export default Post;