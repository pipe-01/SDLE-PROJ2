import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import SmallLink from "../../components/SmallLink";
import Post from "../../components/Post";
import WritePost from "../../components/WritePost";
import useAuth from "../../hooks/useAuth";
import * as C from "./styles";
import { useEffect } from "react";

const api = axios.create({
  baseURL: `http://localhost:${process.env.REACT_APP_API_PORT}/`
})

const Home = () => {
  const { signout, user } = useAuth();
  const navigate = useNavigate();
  const [posts, setPosts] = useState([])
  const [following_users, setFollowingUsers] = useState([])
  const [follower_users, setFollowerUsers] = useState([])

  useEffect( () => {
    /*
    let usercontainers = document.getElementsByClassName("icon-visible-when-hover");
    for (let usercontainer of usercontainers) {
      let icon = usercontainer.getElementsByClassName("icon")[0];
      usercontainer.addEventListener("mouseover", function(){icon.hidden = false;})
      usercontainer.addEventListener("mouseout", function(){icon.hidden = true;})
    }
    */

    async function fetchPosts() {
      let res = await api.get("/posts")
      setPosts(res.data)
    }
    fetchPosts()

    async function fetchFollowing() {
      let res = await api.get("/get_following")
      setFollowingUsers(res.data)
    }
    fetchFollowing()

    async function fetchFollowers() {
      let res = await api.get("/get_followers")
      setFollowerUsers(res.data)
    }
    fetchFollowers()
  } ,[])

  const handleWritePost = async() => {
    let content = document.getElementById("write-post").value
    if (content.length == 0) return;

    await api.get("/publish", { params: { publishContent: content } })
    window.location.reload(false);
  }

  const handleFollow = async() => {
    let follow_username = document.getElementById("user-follow").value
    if (follow_username.length == 0) return;

    let res = await api.get("/follow", { params: { followUsername: follow_username } })
    if (!res.data.success) {
      alert("This user doesn't exist or you already follow him/her")
      return;
    }
    else {
      window.location.reload(false);
    }
  }

  const handleUnfollow = async() => {
    let unfollow_username = document.getElementById("user-unfollow").value
    if (unfollow_username.length == 0) return;
    
    let res = await api.get("/unfollow", { params: { followUsername: unfollow_username } })
    console.log("res.data = ", res.data)
    if (!res.data.success) {
      alert("This user doesn't exist or you don't follow him/her")
      return;
    }
    else {
      window.location.reload(false);
    }
  }

  function createUserComponent(users) {
    let result = []
    users.forEach(user => {
      result.push(<C.UserContainer className="icon-visible-when-hover" key={user}>
        <img src="user_photo.png" alt="User" width="25" />
        {user}
      </C.UserContainer>)
    })
    
    return result
  }

  let postsComponents = []
  posts.forEach(post => {
    postsComponents.push(<Post key={post.username+post.time} Username={post.username} Time={post.time} Content={post.content}/>)
  });

  return (
    <C.Container>
      <C.UserSection>
        <C.UserHeader>
          <img src="user_photo.png" alt="User" width="80" />
          <span >
            <h3>{user.username}</h3>
            <SmallLink Text="Logout" onClick={() => [signout(), navigate("/")]} />
          </span>
        </C.UserHeader>

        <C.FollowContainer>
          <C.SmallTitle>
            Following
          </C.SmallTitle>
          {createUserComponent(following_users)}
        </C.FollowContainer>

        <C.FollowContainer>
          <C.SmallTitle>
            Followers
          </C.SmallTitle>
          {createUserComponent(follower_users)}
        </C.FollowContainer>

      </C.UserSection>
      <C.MiddleSection>
        <h2>Timeline</h2>
        <WritePost Username={user.username} HandleWritePost={handleWritePost}/>
        {postsComponents}
      </C.MiddleSection>

      <C.FollowSection>
        <C.FollowContainer>
          <C.SmallTitle>
            Follow User
          </C.SmallTitle>
          <C.Input id="user-follow" type="text" placeholder="Write a user to follow" width="30px"/>
          <C.ButtonFollow onClick={handleFollow}>Follow</C.ButtonFollow>
        </C.FollowContainer>

        <C.FollowContainer>
          <C.SmallTitle>
            Unfollow User
          </C.SmallTitle>
          <C.Input id="user-unfollow" type="text" placeholder="Write a user to unfollow"/>
          <C.ButtonUnfollow onClick={handleUnfollow}>Unfollow</C.ButtonUnfollow>
        </C.FollowContainer>
      </C.FollowSection>
    </C.Container>
  );
};

export default Home;
