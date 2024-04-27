

<template>
    <div class="explore-container" v-if="renderComponent">
      <div class="explore-left">
        <div v-for="post in posts" v-bind:key="post.id" class="card">
          <div class="explore-user">
            <RouterLink class="link" :to="{path:'/users/' + post.user_id, component: () => ('../views/User.vue')}">
              <img :src="post.profile_photo"> 
              <p >{{ post.username }}</p>
            </RouterLink>
          </div>
  
          <div class="explore-img">
              <img :src="post.photo">
          </div>
          
          <div class="explore-desc">
              {{ post.caption }}
          </div>
  
          <div class="explore-stats">
                <div class="likes"  @click="() => likedPost(post.id)">
                    <img src="heart.png" alt="red heart, post liked">
                    <div><span>{{ post.likes }}</span> likes</div>
                </div>
  
                <p class="explore-date">{{ post.created_on }}</p>
          </div>
        </div>   
      </div>
      <div class="explore-right"> 
        <RouterLink  class="explore-btn" to="/posts/new">New Post</RouterLink>
      </div>   
    </div>
  </template>





  <script setup>
    import {ref, onMounted} from 'vue'
    import { RouterLink, useRouter } from "vue-router"
    const token = localStorage.getItem("token")
    
    const renderComponent = ref(true)
    let posts= ref([])
    let csrf_token = ref("")
    let result = ref([])
  
    const getCsrfToken = () => {
          fetch('/api/v1/csrf-token')
          .then(res => res.json())
          .then(data => {
              csrf_token.value = data.csrf_token
          })
      }
  
    onMounted(() => {
        fetchPosts().then(data => posts.value = data)
        getCsrfToken()
    })
  
    const forceRender = async () => {
          renderComponent.value = false;
          await nextTick();
          renderComponent.value = true;
    };
  
    const fetchUser = async(id) => {
          
          const res = await fetch(`/api/v1/users/${id}`)
          const data = await res.json()
          return data
          
      }
  
    const fetchPosts = async() => {
          fetch('/api/v1/posts', {
              method: 'GET',
              headers: {
                  'X-CSRFToken': csrf_token.value,
                  Authorization: 'Bearer ' + jwt_token.value,                
              }
          })
          .then((response) => response.json())
          .then((data) => {
              console.log(data)
              for(const post of data){
                  posts.value.push(post)
              }
          })
      }
  
    
    const likedPost = (postID) => {
          const alert = document.querySelector("#alert");
          fetch(`/api/v1/posts/${id}/like`, {
                  method: 'POST',
                  headers: {
                      'X-CSRFToken': csrf_token.value,
                      Authorization: 'Bearer ' + jwt_token.value,
                  }
                  }).then(function (response) {
                      return response.json();
                  }).then(function (data) {
                  // display a success message
                      console.log(data);
                      alert.style.display = 'block'
                      alert.textContent = data.message ? data.message : data.errors[0]
                  }).catch(function (error) {
                      console.log(error);
                  });
      }
     

  </script>






  <style>
  .explore-container {
    display: flex;
    margin-top: 50px;
    height: 100vh;
    width: 100vw;
  }
  
  .explore-left {
    width: 100%;
    display: flex;
    flex-direction: column;
    flex:3;
    margin: 0 auto;
  }
  
  .card {
    display: flex;
    flex-direction: column;
    padding: 15px;
    margin-right: auto;
    margin-left: auto;
    width: 700px;
    margin-bottom: 10px;
    gap: 10px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0);
  }
  
  .explore-user {
    display: flex;
    align-items: center;
    gap: 10px;
    text-decoration: none;
    font-weight: 500;
    color: rgb(83, 83, 83);
    width: 20px;
    border-radius: 50%;
    object-fit: cover;
    
  }
  
  .explore-img {
    width: 100%;
    height: 500px;
    object-fit: contain;
  }
  
  .explore-stats {
    width: 100%;
    display: flex;
    justify-content: space-between;
  }
  
  .explore-likes {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 500;
    width: 15px;
    object-fit: contain;
  }
  
  .explore-btn {
    flex: 1;
    display: flex;
    justify-content: center;
    text-decoration: none;
    color: #fff;
    background: rgb(42, 174, 207);
    height: 30px;
    width: 200px;
    text-align: center;
    border-radius: 3px;
  }
  
  .explore-date {
    font-weight: 500;
  }
  </style>