<template>
  <div class="d-flex flex-column align-items-center">
    <button class="btn btn-primary button-arrow" @click="isCollapsed = !isCollapsed" style="border-radius: 20px; background: linear-gradient(to right, #6a11cb, #2575fc); padding: 0.75rem 2rem;">
      Challenge erstellen <i :class="isFormVisible ? 'bi bi-chevron-up' : 'bi bi-chevron-down' " class="ms-2"></i>
    </button>

    <div :class="{'collapse': isCollapsed, 'show': !isCollapsed, 'w-100': true, 'mt-3': true}">
      <div class="card card-body" style="border-radius: 20px;">
        <form @submit.prevent="createChallenge" novalidate :class="{'was-validated': needsValidation}" class="needs-validation d-flex flex-column align-items-center">
          <div class="mb-3 w-100">
            <label class="form-label" for="challenge_name">Challenge Name</label>
            <input class="form-control" required id="challenge_name" type="text" v-model="challengeForm.challenge_name">
            <div class="invalid-feedback">
              Challenge Name muss befüllt sein.
            </div>
          </div>
          <div class="mb-3 w-100">
            <label class="form-label" for="description" >Beschreibung</label>
            <textarea class="form-control" required id="description" v-model="challengeForm.description"></textarea>
            <div class="invalid-feedback">
              Challenge Beschreibung muss befüllt sein.
            </div>
          </div>
          <div class="mb-3 w-100">
            <label class="form-label" for="reward" >Preis</label>
            <input class="form-control" type="text" id="reward" v-model="challengeForm.reward">
          </div>
          <div class="mb-3 w-100">
            <label class="form-label" for="friend">Select Friend</label>
            <select class="form-select" id="friend" v-model="challengeForm.friendId" aria-label="Default select example">
              <option value="">Wähle einen Freund aus</option>
              <option v-for="friend in friends" :key="friend.id" :value="friend.id">{{ friend.name }}</option>
            </select>
          </div>
          <button type="submit" class="btn btn-success w-100">
            {{ challengeForm.friendId ? 'Freund herausfordern' : 'Challenge-Link erstellen' }}
          </button>
          <div v-if="errorMessage != ''" class="mt-2 text-danger">{{errorMessage}}</div>
          <div v-if="successMessage != ''" class="mt-2 text-success">{{successMessage}}</div>
        </form>
      </div>
    </div>
  </div>
  <LinkModal ref="linkModal"/>
</template>
  
<script setup>
import { ref, onMounted } from 'vue';
import { useStore } from '../stores/store'
import LinkModal from '@/components/LinkModal.vue';
import challengeService from "../services/challenge.service.js";
import friendshipService from "../services/friendship.service.js";

const store = useStore()

const errorMessage = ref('')
const successMessage = ref('')
const needsValidation = ref(false)
const challengeId = ref('')

const isCollapsed = ref(true);
const linkModal = ref(null);
const isFormVisible = ref(false);
const friends = ref('')
const challengeForm = ref({
  user_id: store.user.uid,
  challenge_name: '',
  description: '',
  reward: null,
  friend_id: null,
  hashtags_list: null,
  chatgpt_check: false,
  email_check: false,
});


const createChallenge = async () => {
  needsValidation.value = true

  if(!challengeForm.value.challenge_name || !challengeForm.value.description){
    console.log("Required fields are missing:", challenge.value);
    return;
  }
  if (challengeForm.value.friend_id === '') challengeForm.value.friend_id = null
  if (challengeForm.value.reward === '') challengeForm.value.reward = null
  console.log(challengeForm.value)
  const res = await challengeService.createChallenge(challengeForm.value)
  console.log("Created challenge with ID:", res.data)
  if (res.status == 200) {
    challengeId.value = res.data
    if (!challengeForm.value.friend_id) linkModal.value.showLinkModal(challengeId.value);
    needsValidation.value = false
    errorMessage.value = ''
    successMessage.value = "Challenge wurde erfolgreich erstellt."
    challengeForm.value = {
      user_id: store.user.uid,
      challenge_name: '',
      description: '',
      reward: null,
      friend_id: null,
      hashtags_list: null,
      chatgpt_check: false,
      email_check: false,
      overlay: false,
    };
  }
  isCollapsed.value = false;
};


const getFriends = async () => {
  try {
    friends.value = await friendshipService.getFriend(store.user.uid).data
  } catch (error) {
    alert("Could not get Friends.", error.response);
  }
}

onMounted(() => {
  getFriends()
});
</script>
  
<style scoped>
/* css */
</style>