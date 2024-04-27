<template>
    <div class="registerContainer">
        <h1>Register</h1>
        <div v-if = "response_type == 'error'" class="alert alert-danger">
            <ul>
                <li v-for="error in response.errors">{{ error }}</li>
            </ul>
        </div>

        <form @submit.prevent="registerUser" id="registrationForm" class="formContainer">
            <div class="formGroup">
                <label for="username">Username</label>
                <input type="text" v-model="username" required />
            </div>

            <div class="formGroup">
                <label for="password">Password</label>
                <input type="password" v-model="password" required />
            </div>

            <div class="formGroup">
                <label for="firstName">First Name</label>
                <input type="text" v-model="firstName"  />

            </div>

            <div class="formGroup">
                <label for="lastName">Last Name</label>
                <input type="text" v-model="lastName"  />
            </div>

            <div class="formGroup">
                <label for="email">Email</label>
                <input type="email" v-model="email" required />
            </div>

            <div class="formGroup">
                <label for="location">Location</label>
                <input type="text" v-model="location" />
            </div>

            <div class="formGroup">
                <label for="biography">Biography</label>
                <textarea v-model="biography" ></textarea>
            </div>
            
            <div class="formGroup">
                <label for="profilePic">Photo</label>
                <input type="file" @change="handleFileUpload" />
            </div>
            
    
            <button type="submit" class="submitButton">Register</button>
        </form>

    </div>


</template>

<script setup>
    import { ref } from 'vue';
    import { useRouter } from 'vue-router';

    const router = useRouter();

    const csrf_token = ref('');
    const response = ref([]);
    const response_type = ref('');
    const username = ref('');
    const password = ref('');
    const email = ref('');

    function getCsrfToken() {
    fetch('/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
        csrf_token.value = data.csrf_token;
        });
    }

    const selectedFile = ref(null); 

    const handleFileUpload = (event) => {
    selectedFile.value = event.target.files[0]; 
    };

    const registerUser = async () => {
    try {
        const registrationForm = document.getElementById('registrationForm');
        const form_data = new FormData(registrationForm);

        const response = await fetch('/api/v1/auth/register', {
        method: 'POST',
        body: form_data,
        headers: {
            'X-CSRFToken': csrf_token.value,
        },
        });

        const data = await response.json();

        if (data.hasOwnProperty('errors')) {
        response_type.value = 'error';
        response.value = data.errors;
        } else {
        response_type.value = 'success';
        alert('Registration successful!');
        router.push({ path: '/login' });
        }
    } catch (error) {
        console.log('Error registering user:', error);
    }
    };

    getCsrfToken(); // Obtain the CSRF token when the component is set up
</script>

<!-- css syle for regestir form -->
<style>

body{
    background-color: rgb(244, 235, 224);
}

h1{
    margin-right: 250px;
    margin-top: 50px;
    font-size: 30px;
    color: rgb(85, 85, 85);
}

.registerContainer{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;

}

.formContainer{
    background-color: white;
    width: 80%; 
    max-width: 400px; 
    background-color: white;
    padding: 20px; 
    border: 1px solid #ccc; 
    border-radius: 5px; 
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}

.formGroup{
    display: flex;
    flex-direction: column;
    padding: 10px;
}

.formGroup input{
    border-style: none;
    border: 1px solid #ccc; 
    border-radius: 3px; 
}

.formGroup textarea{
    border-style: none;
    border: 1px solid #ccc; 
    border-radius: 3px; 
}

label{
    font-weight: bold;
    color: rgb(85, 85, 85);
    margin-bottom: 5px;
}

.submitButton{
    border-style: none;
    background-color: rgb(97, 224, 97);
    color: white;
    border-radius: 3px;
    width: 100%;
    height: 30px;
    margin-top: 20px;
}

.submitButton:hover{
    background-color: rgb(53, 183, 140);
}
</style>
