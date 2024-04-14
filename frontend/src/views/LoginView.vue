<template>
    <div class="container fullpage d-flex flex-grow-1">
        <div class="col-md-5 col m-auto">
            <h1 class="h2 mb-3">Anmelden / Registrieren</h1>
            <form @submit.prevent="signInWithEmail" :class="{'was-validated': wasValidated}" class="needs-validation" novalidate>
                <div class="mb-3">
                    <input class="form-control" id="emailSignUp" type="email" required v-model="user.email" placeholder="E-mail" />
                    <div class="invalid-feedback">
                        Bitte gib eine gültige E-Mail Adresse ein.
                    </div>
                </div>
                <div class="mb-3">
                    <input class="form-control" id="passwordSignUp" type="password" required v-model="user.password" placeholder="Passwort"/>
                    <div class="invalid-feedback">
                        Passwort muss befüllt sein.
                    </div>
                </div>
                <button class="btn btn-primary col-md-12" type="submit">Anmelden</button>
                <div class="mt-1 text-danger">{{errorMessage}}</div>
            </form>
            <br>
            <div class="text-center">oder</div>
            <br>
            <button class="btn btn-primary col-md-12" @click="signInWithGoogle">Mit Google anmelden</button>
        </div>
    </div>
</template>

<script setup>
import router from '../router/index.js';
import { ref, watch } from 'vue';
import { useStore } from '../stores/store'
import { useRoute } from 'vue-router';
import { getAuth, linkWithCredential, EmailAuthProvider, GoogleAuthProvider, signInWithPopup } from "https://www.gstatic.com/firebasejs/10.10.0/firebase-auth.js";



const user = ref({
    email: '',
    password: ''
})


const errorMessage = ref('')
const wasValidated = ref(false)
function isEmailValid(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}
const store = useStore()
const route = useRoute()
store.challengeId = route.query.challengeId

async function signInWithGoogle(){
    const provider = new GoogleAuthProvider();
    signInWithPopup(getAuth(), provider)
    .then((result) => {
        linkAccount(GoogleAuthProvider.credentialFromResult(result));
    });
    }

async function signInWithEmail(){
    wasValidated.value = true
    if (!user.value.email || !user.value.password) {
        errorMessage.value = "Bitte fülle alle Felder aus.";
        return
    }
    if (!isEmailValid(user.value.email)) {
        errorMessage.value = "Bitte gib eine gültige E-Mail Adresse ein.";
        return;
    }
    linkAccount(EmailAuthProvider.credential(user.value.email, user.value.password));
}

async function linkAccount(credentials){
    linkWithCredential(getAuth().currentUser, credentials)
        .then((usercred) => {
            console.log("Anonymous account successfully upgraded", user);
            store.user = usercred.user;
            store.isLinked = true;
            router.push({name: 'home'});
        }).catch((error) => {
            console.log("Error upgrading anonymous account", error);
            errorMessage.value = error;
    });
}

watch(() => store.isLinked, (isLinked) => {
  if (isLinked) {
    router.push({name: 'home'});
  }
});

</script>