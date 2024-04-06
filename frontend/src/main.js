import './styles/main.scss'
import 'bootstrap/dist/css/bootstrap.min.css'
import bootstrap from 'bootstrap/dist/js/bootstrap.bundle.min.js'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { initializeApp } from "firebase/app";
import { getAuth, onAuthStateChanged, signInAnonymously } from "firebase/auth";

import App from './App.vue'
import router from './router'

// import { getAnalytics } from "firebase/analytics";
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyArJSUxu_ouR5ywan477n5CYC7N2JncE40",
    authDomain: "challengeaccepted-db871.firebaseapp.com",
    projectId: "challengeaccepted-db871",
    storageBucket: "challengeaccepted-db871.appspot.com",
    messagingSenderId: "267560795363",
    appId: "1:267560795363:web:c727a195f9babf555259d6",
    measurementId: "G-268HS0CD8Y"
  };

// Initialize Firebase
initializeApp(firebaseConfig);
// const analytics = getAnalytics(app);

const app = createApp(App)
//  BOOTSTRAP init
app.use(bootstrap)
app.use(createPinia())
app.use(router)


const auth = getAuth();
import { useStore } from './stores/store'
const store = useStore()

onAuthStateChanged(auth, (user) => {
    if (!user) {
        signInAnonymously(auth).then((result) => {
            store.user = result.user;
            store.isLinked = false;
            console.log(`User is signed in anonymously with UID: ${result.user.uid}`);
            localStorage.setItem('user', JSON.stringify(result.user));
        })
        .catch((error) => {
            console.error(`Error during anonymous sign-in: ${error.message}`);
        });
    } else {
        store.isLinked = true;
        console.log(`User is signed in linked with UID: ${user.uid}`);
        localStorage.setItem('user', JSON.stringify(user.toJSON()));
        store.user = user;
        store.isLinked = true;
    }
});


app.mount('#app')
