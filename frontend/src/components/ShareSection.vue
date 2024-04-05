<template>
     <div class="modal fade modal-md" :id="'share' + challenge.id" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h2 class="modal-title h5" id="exampleModalLabel">Challenge weitergeben</h2>
                    <button class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="createChallenge()">
                        <div class="mb-3">
                        <label class="form-label" for="friend">Freund auswählen *</label>	
                            <select id="friend" class="form-select" required v-model="newChallenge.friend_id" aria-label="Default select example">
                            <option disabled value="">Wähle einen Freund aus</option>
                            <option v-for="friend in friends" :key="friend.user_id" :value="friend.user_id">{{ friend.username }}</option>
                            </select>
                            <div class="invalid-feedback">
                            Freund muss ausgewählt sein.
                            </div>
                        </div>
                        <div class="form-check mb-3">
                            <input type="checkbox" id="chatgpt_check" class="form-check-input" v-model="newChallenge.email_check">
                            <label for="checkbox" class="form-check-label">Email an Freund senden</label>
                        </div>
                        <button class="btn btn-primary">Freund herausfordern</button>
                        <div v-if="errorMessage != ''" class="mt-2 text-danger">{{errorMessage}}</div>
                        <div v-if="successMessage != ''" class="mt-2 text-success">{{successMessage}}</div>   	
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps, toRef } from 'vue';
import challengeService from '../services/challenge.service.js'
import friendshipService from '../services/friendship.service.js'
import {useStore} from '../stores/store'
const store = useStore()

const props = defineProps(['challenge']);
const challenge = toRef(props, 'challenge');
const friends = ref([])
const errorMessage = ref('')
const successMessage = ref('')

const newChallenge = ref({
    user_id: store.user.id,
    challenge_name: challenge.value.title,
    friend_id: null,
    description: challenge.value.description,
    hashtags_list: challenge.value.hashtags[0] ? challenge.value.hashtags.map(hashtag => hashtag.text).join(',') : null,
    reward: challenge.value.reward,
    chatgpt_check: false,
    email_check: false,
  });

const createChallenge = async () => {

  try {
    if (challenge.value.receiver_id == newChallenge.value.friend_id ) {
      errorMessage.value = "Du kannst nicht der selben Person die Challenge schicken."
      return
    }
    const res = await challengeService.createChallenge(newChallenge.value)
    if (res.status == 200) {
      errorMessage.value = ''
      successMessage.value = "Challenge wurde erfolgreich erstellt."
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

getFriends()
</script>

