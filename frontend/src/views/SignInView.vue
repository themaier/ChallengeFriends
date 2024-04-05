<template>
    <div class="container fullpage d-flex flex-grow-1">
        <div class="col-md-5 col m-auto">
            <h1 class="h2 mb-3">Anmelden</h1>
            <form @submit.prevent="login" :class="{'was-validated': needsValidation}" class="needs-validation" novalidate>
                <div class="mb-3">
                    <label class="form-label" for="username">Username *</label>
                    <input class="form-control" id="username" type="text" required placeholder="Username" v-model="user.username"/>
                    <div class="invalid-feedback">
                        Username muss befüllt sein.
                    </div>
                </div>
                <div class="mb-3">
                    <label class="form-label" for="password">Passwort *</label>
                    <input class="form-control" id="password" type="password" required placeholder="Passwort" v-model="user.password"/>
                    <div class="invalid-feedback">
                        Passwort muss befüllt sein.
                    </div>
                </div>
                <button class="btn btn-primary" type="submit">Anmelden</button>
                <div class="mt-1 text-danger">{{errorMessage}}</div>
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import userService from '../services/user.service.js'
import router from '../router/index.js'
import {useStore} from '../stores/store'
const user = ref({
    username: '',
    password: ''
})
const errorMessage = ref('')
const needsValidation = ref(false)
const store = useStore()

async function login(){
    needsValidation.value = true
    if (!user.value.username || !user.value.password) {
        return
    }
    try {
        if (store.challengeId) {
            user.value.challengeId = store.challengeId;
        }
        const response = await userService.login(user.value)
        
        if (response.status == 200) {
            router.push({name: 'home'});
            store.user = response.data
            localStorage.setItem('loggedIn', 'true');
            localStorage.setItem('user', JSON.stringify(response.data));
            store.loggedIn = true
            store.challengeId = null
            delete user.value.challengeId;
        }       
    } catch(error) {
        if(error.response.status == 401){
            errorMessage.value = "Username oder Passwort falsch!"
        }
        else{
            errorMessage.value = "Ein Fehler ist aufgetreten! Bitte versuche es später erneut."
        }
    }
}
</script>