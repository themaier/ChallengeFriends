<template>
<main>
<div class="container-md">
  <h1 class="my-4">Challenge erstellen</h1>
    <div class="col-md-5 col mt-5 m-auto">
        <form @submit.prevent="createChallenge" novalidate :class="{'was-validated': needsValidation}" class="needs-validation">
            <div class="mb-3">
                <label class="form-label" for="challengename">Challenge Name *</label>
                <input class="form-control" id="challengename" required type="text" v-model="challenge.challenge_name" placeholder="z.B. Spexen" />
                <div class="invalid-feedback">
                  Challenge Name muss befüllt sein.
                </div>
            </div>
            <div class="mb-3">
                <label for="description">Beschreibung *</label>
                <input type="text" class="form-control" required id="description" v-model="challenge.description" placeholder="z.B. Wie macht der Bär?" >
                <div class="invalid-feedback">
                  Challenge Beschreibung muss befüllt sein.
                </div>
            </div>

            <div class="mb-3">
                <label for="hashtags">Hashtag (optional)</label>
                <input type="text" class="form-control" id="hashtags" v-model="challenge.hashtags_list" aria-describedby="hashtagHelp" placeholder="z.B. WebEngineering">
                <div id="hashtagHelp" class="form-text">
                  Hashtags müssen mit Komma getrennt werden und dürfen keine Leerzeichen sowie # enthalten.
                </div>
            </div>

            <div class="mb-3">
                <label for="reward">Reward (optional)</label>
                <input type="text" class="form-control" id="reward" v-model="challenge.reward">
            </div>
            <div class="form-check mb-3">
              <input type="checkbox" id="chatgpt_check" class="form-check-input" v-model="challenge.chatgpt_check">
              <label for="checkbox" class="form-check-label">Legal check mit ChatGPT</label>
            </div>
            <div class="form-check mb-3">
              <input type="checkbox" id="chatgpt_check" class="form-check-input" v-model="challenge.email_check">
              <label for="checkbox" class="form-check-label">Email an Freund senden</label>
            </div>
            <div class="mb-3">
              <label class="form-label" for="friend">Freund auswählen</label>	
                <select id="friend" class="form-select" v-model="challenge.friend_id" aria-label="Default select example">
                  <option value="">Wähle einen Freund aus</option>
                  <option v-for="friend in friends" :key="friend.user_id" :value="friend.user_id">{{ friend.username }}</option>
                </select>
                <div class="invalid-feedback">
                  Freund muss ausgewählt sein.
                </div>
            </div>
            <br>
            <button type="submit" class="btn btn-primary" style="text-align: center">
              {{ challenge.friend_id ? 'Freund herausfordern' : 'Challenge-Link erstellen' }}
            </button>
            <button id="invisibleOpenModalButton" style="visibility: hidden;" data-bs-toggle="modal" data-bs-target="#staticBackdrop"></button>
            <div v-if="errorMessage != ''" class="mt-2 text-danger">{{errorMessage}}</div>
            <div v-if="successMessage != ''" class="mt-2 text-success">{{successMessage}}</div>
            <div v-if="challenge.chatgpt_check">
              <!-- <br>
              <CheckoutItem />
              <CheckoutPayment /> -->
            </div>
        </form>
    </div>
</div>
<!-- Modal -->
<div class="modal fade" id="staticBackdrop" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="staticBackdropLabel">Challenge Link</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        http://{{ipv4}}:3000/registrieren?challengeId={{challengeId}}
      </div>
      <div class="modal-footer d-flex justify-content-center">
        <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="copyTextToClipboard()">Kopieren</button>
      </div>
    </div>
  </div>
</div>
<div id="paypal-button-container"></div>
</main>
</template>

<script setup>
import { ref } from 'vue'
import challengeService from "../services/challenge.service.js";
import friendshipService from "../services/friendship.service.js";
import { useStore } from '../stores/store'
import CheckoutPayment from '../components/CheckoutPayment.vue'
import CheckoutItem from '../components/CheckoutItem.vue'
const ipv4 = import.meta.env.VITE_IPV4 || 'localhost';
const errorMessage = ref('')
const successMessage = ref('')
const needsValidation = ref(false)
const challengeId = ref('')
const store = useStore()
const challenge = ref({
    user_id: store.user.id,
    challenge_name: '',
    friend_id: null,
    description: '',
    hashtags_list: null,
    reward: null,
    chatgpt_check: false,
    email_check: false,
    overlay: false,
  });

const friends = ref('')

const createChallenge = async () => {
  try {
    needsValidation.value = true

    if(!challenge.value.challenge_name || !challenge.value.description){
      return
    }
    if (challenge.value.friend_id === '') challenge.value.friend_id = null
    if (challenge.value.hashtags_list === '') challenge.value.hashtags_list = null
    if (challenge.value.reward === '') challenge.value.reward = null
    if (challenge.value.hashtags_list)	{
      challenge.value.hashtags_list = challenge.value.hashtags_list.replace(/[#\s]/g, '')
    }
    const res = await challengeService.createChallenge(challenge.value)
    if (res.status == 200) {
      if (!challenge.value.friend_id) document.getElementById('invisibleOpenModalButton').click();
      challengeId.value = res.data
      needsValidation.value = false
      errorMessage.value = ''
      successMessage.value = "Challenge wurde erfolgreich erstellt."
      challenge.value = {
        user_id: store.user.id,
        challenge_name: '',
        friend_id: null,
        description: '',
        hashtags_list: null,
        reward: null,
        chatgpt_check: false,
        email_check: false,
      };
      
    }
  } catch (error) { 
    successMessage.value = ''
    errorMessage.value = ''
    if (error.response && error.response.status === 406) {
      errorMessage.value= error.response.data.detail
    } else {
        errorMessage.value="Challenge erstellen hat nicht funktioniert. Bitte versuche es später erneut."
    }
  }
}

const getFriends = async () => {
  try {
    const res = await friendshipService.getFriend(store.user.id)
    if (res.status == 200) {
      friends.value = res.data
    }
  } catch (error) {
    if (error.response && error.response.status === 406) {
      alert("The challenge is illegal.")
    } else {
        alert("Error running rest-call:", error.message);
    }
  }
}

const copyTextToClipboard = () => {
  navigator.clipboard.writeText(`http://${ipv4}:3000/registrieren?challengeId=${challengeId.value}`).then(function() {
  }).catch(err => {
    console.error('Error in copying link: ', err);
  });
}

getFriends()

</script>