<template>
    <div class="container">
        <div class="form-box">
            <h3 class="header-text">Register</h3>

            <div v-if = "fetchResponseType == 'success'" class="alert alert-success">
                {{ fetchResponse.message }}
            </div>

            <div v-if = "fetchResponseType == 'danger'" class="alert alert-danger">
                <ul>
                    <li v-for="error in fetchResponse.errors">
                        {{ error }}
                    </li>
                </ul>
            </div>

            <form @submit.prevent = "register" id = "RegistrationForm">
                <div class = "formInfo">
                    <div class="form-group mb-3">
                        <label for="username" class="form-label">Username</label>
                        <input type="text" name="username" class="formcontrol" />
                        <small v-if="formData.username === ''" class="text-danger">Username is required</small>
                    </div>

                    <div class="form-group mb-3">
                        <label for="password" class="form-label">Password</label>
                        <input type="text" name="password" class="formcontrol" />
                        <small v-if="formData.password === ''" class="text-danger">Password is required</small>
                    </div>

                    <div class="form-group mb-3">
                        <label for="firstName" class="form-label">Firstname</label>
                        <input type="text" name="firstName" class="formcontrol" />
                        <small v-if="formData.firstName === ''" class="text-danger">First Name is required</small>
                    </div>

                    <div class="form-group mb-3">
                        <label for="lastName" class="form-label">Lastname</label>
                        <input type="text" name="lastName" class="formcontrol" />
                        <small v-if="formData.lastName === ''" class="text-danger">Last Name is required</small>
                    </div>

                    <div class="form-group mb-3">
                        <label for="email" class="form-label">Email</label>
                        <input type="text" name="email" class="formcontrol" />
                        <small v-if="formData.email === ''" class="text-danger">Email is required</small>
                    </div>

                    <div class="form-group mb-3">
                        <label for="location" class="form-label">Location</label>
                        <input type="text" name="location" class="formcontrol" />
                        <small v-if="formData.location === ''" class="text-danger">Location is required</small>
                    </div>

                    <div class="form-group mb-3">
                        <label for="biography" class="form-label">Biography</label>
                        <textarea name="biography" class="formcontrol" ></textarea>
                        <small v-if="formData.biography === ''" class="text-danger">A Biography is required</small>

                    </div>

                    <div class="form-group mb-3">
                        <label for="photo" class="form-label">Photo</label>
                        <input type="file" id="photo" name="photo" class="formcontrol" accept=".jpg,.jpeg,.png" />
                        <small v-if="formData.profile_photo === null" class="text-danger"> A photo is required</small>
                    </div>

                    <button type ="submit">Register</button>

                    <div v-if="registrationError" class="text-danger">{{ registrationError }}</div>
                </div>
            </form>
        </div>
    </div>

</template>


<script setup>
    import { ref, onMounted } from "vue";
    
    let csrf_token = ref("")
    let fetchResponseType = ref("")
    let fetchResponse = ref("")


    function getCsrfToken() {
        fetch('/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
        console.log(data);
        csrf_token.value = data.csrf_token;
        })
    }
    onMounted(() => {
        getCsrfToken()
    })
    function register(){
        let RegistrationForm = document.querySelector("#RegistrationForm")
        let formData = new FormData(RegistrationForm)
        fetch("/api/v1/register", {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrf_token.value
            }
        })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            console.log(data);
            fetchResponse.value = data
            
            if(data.hasOwnProperty('errors')) {
                fetchResponseType.value = "danger"
            } else {
                fetchResponseType.value = "success"
            }
        })
        .catch(function (error) {
            console.log(error);
        });
    }
</script>









<style>
    
    *{
        -moz-box-sizing: border-box; 
        -webkit-box-sizing: border-box; 
        box-sizing: border-box; 
    }
    .header-text{
        font-weight: bold;
    }
    .container{
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 50px;
    }

    form{
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 2px 2px 8px rgb(109, 111, 101);
        background-color: white;
        padding: 50px;
    }
    .form-box{
        max-width: 500px;
        width: 100%;
    }
    .form-group{
        display: flex;
        margin-bottom: 15px;
        flex-direction: column;
    }
    .form-label{
        font-weight: bold;
    }

    button{
        background-color: rgb(10, 255, 47);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        padding: 6px;
        width: 100%;
        margin-top: 10px;
    }
    button:hover{
        background-color: rgb(0, 255, 47);
        color: white;
        transition: all 0.9s;
    }
</style>