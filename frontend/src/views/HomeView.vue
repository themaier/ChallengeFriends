<template>
  <div>
    <div class="container-md">
      <h1 class="my-4">Meine Challenges</h1>
    </div>
    <div class="container-md bg-body-secondary py-3 rounded">
      <h2 class="mb-4">Ausstehende Challenges</h2>
      <div v-if="!pendingChallenges[0]">Keine ausstehenden Challenges zurzeit!</div>
      <div v-if="pendingChallenges[0]" class="container-md bg-body-tertiary rounded py-2">
        <ul class="px-0 my-0">
          <li class="row align-items-center py-3 gy-2 gy-lg-0" v-for="pendingChallenge in pendingChallenges" :key="pendingChallenge.id">
            <div class="col-lg-2">{{pendingChallenge.title}}</div>
            <div class="col-lg">{{pendingChallenge.description}}</div>
            <div v-if="pendingChallenge.reward" class="col-lg-2">Reward: {{pendingChallenge.reward}}</div>
            <div v-if="pendingChallenge.hashtags[0]" class="col-lg-2"><RouterLink :to="{ name: 'trending', query: { hashtag: hashtag.text } }" v-for="hashtag in pendingChallenge.hashtags" :href="'?hashtag='+ hashtag.text" :key="hashtag.id" class="link-primary link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover">#{{hashtag.text}}</RouterLink></div>
            <div class="col-3 align-self-end d-flex  justify-content-lg-end d-flex-column">
              <button class="btn btn-success btn-block" @click="acceptChallenge(pendingChallenge.id)">Annehmen</button>
              <button class="btn btn-danger btn-block offset-1" @click="declineChallenge(pendingChallenge.id)">Ablehnen</button>
            </div>
          </li>
        </ul>
      </div>
    </div>

    <div class="container-md bg-body-secondary py-3 rounded mt-4">
      <h2 class="mb-4">Aktive Challenges</h2>
      <div v-if="!acceptedChallenges[0]">Keine aktiven Challenges zurzeit!</div>
      <div v-if="acceptedChallenges[0]" class="container-md bg-body-tertiary rounded py-2">
        <ul class="px-0 my-0">
          <li  class="row align-items-center py-3 gy-2 gy-lg-0" v-for="acceptedChallenge in acceptedChallenges" :key="acceptedChallenge.id">
            <div class="col-lg-2">{{acceptedChallenge.title}}</div>
            <div class="col-lg">{{acceptedChallenge.description}}</div>
            <div v-if="acceptedChallenge.reward" class="col-lg-2">Reward: {{acceptedChallenge.reward}}</div>
            <div v-if="acceptedChallenge.hashtags[0]" class="col-lg-2"><RouterLink :to="{ name: 'trending', query: { hashtag: hashtag.text } }" v-for="hashtag in acceptedChallenge.hashtags" :href="'?hashtag='+ hashtag.text" :key="hashtag.id" class="link-primary link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover">#{{hashtag.text}}</RouterLink></div>
            <div class="col-3 align-self-end d-flex  justify-content-lg-end d-flex-column">
              <button class="btn btn-primary" data-bs-toggle="modal" :data-bs-target="'#proveModal'+acceptedChallenge.id">Abschließen</button>
            </div>
          </li>
        </ul>
      </div>
    </div>

    <div class="container-md">
      <h1 class="my-4">Andere Challenges</h1>
    </div>
    <div class="container-md bg-body-secondary py-3 rounded mt-4">
      <h2 class="mb-4">Freunde</h2>
      <div v-if="!createdChallenges[0]">Freunde habe zurzeit keine aktiven Challenges von dir!</div>
      <div v-if="createdChallenges[0]" class="container-md bg-body-tertiary rounded py-2">
        <ul class="px-0 my-0">
          <li  class="row align-items-center py-3 gy-2 gy-lg-0" v-for="createdChallenge in createdChallenges" :key="createdChallenge.id">
            <div class="col-lg-1"> <RouterLink :to="{ name: 'friendProfile', params: { id: createdChallenge.receiver_user_id } }" class="link-dark fw-bold link-offset-2 link-underline-opacity-0 link-underline-opacity-100-hover">{{ createdChallenge.receiver_user_name }}</RouterLink></div>
            <div class="col-lg-2">{{createdChallenge.title}}</div>
            <div class="col-lg">{{createdChallenge.description}}</div>
            <div v-if="createdChallenge.reward" class="col-lg-2">Reward: {{createdChallenge.reward}}</div>
            <div v-if="createdChallenge.hashtags[0]" class="col-lg-2"><RouterLink :to="{ name: 'trending', query: { hashtag: hashtag.text } }" v-for="hashtag in createdChallenge.hashtags" :href="'?hashtag='+ hashtag.text" :key="hashtag.id" class="link-primary link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover">#{{hashtag.text}}</RouterLink></div>
            <div v-if="createdChallenge.status=='pending'" class="col-lg-3 text-lg-end">Antwort ausstehend</div>
            <div v-if="createdChallenge.status=='accepted'" class="col-lg-3 text-lg-end">Challenge accepted</div>
          </li>
        </ul>
      </div>
    </div>
  </div>

  <ProveChallengeModal :challenges="acceptedChallenges" @uploadedSucessfully="uploadedSucessfully()" :success="success"></ProveChallengeModal>


    <div v-if="success" class="animation">
      <div class="firework"></div>
      <div class="firework"></div>
      <div class="firework"></div>
      <div class="success-animation">
        <svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52"><circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none" /><path class="checkmark__check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8" /></svg>
      </div>
    </div>

</template>

<script setup>
import challengeService from "../services/challenge.service";
import {useStore} from '../stores/store'
import {ref} from 'vue'
import ProveChallengeModal from '../components/ProveChallengeModal.vue'
const store = useStore()
const pendingChallenges = ref([])
const acceptedChallenges = ref([])
const createdChallenges = ref([])
const success = ref(false)

const uploadedSucessfully = () => {
  success.value = true
  setTimeout(() => {
    success.value = false
        document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());
        document.body.classList.remove('modal-open');
        document.body.style.paddingRight = '';
        document.body.style.overflow = '';
  }, 2300);
  getAcceptedChallenges()
}
const getAcceptedChallenges = async () => {
  try {
    const res = await challengeService.getAcceptedChallenges(store.user.id)
    if (res.status == 200) {
      acceptedChallenges.value = res.data
    }
  } catch (error) {
    console.log(error)
  }
}

const getPendingChallenges = async () => {
  try {
    const res = await challengeService.getPendingChallenges(store.user.id)
    if (res.status == 200) {
      pendingChallenges.value = res.data
      console.log(pendingChallenges.value)
    }
  } catch (error) {
    console.log(error)
  }
}

const getCreatedChallenges = async () => {
  try {
    const res = await challengeService.getCreatedChallenges(store.user.id)
    if (res.status == 200) {
      createdChallenges.value = res.data
    }
  } catch (error) {
    console.log(error)
  }
}

const acceptChallenge = async (challengeId) => {
  try {
    const res = await challengeService.acceptChallenge(challengeId)
    if (res.status == 200) {
      getAcceptedChallenges()
      getPendingChallenges()
    }
  } catch (error) {
    console.log(error)
  }
}

const declineChallenge = async (challengeId) => {
  try {
    const res = await challengeService.declineChallenge(challengeId)
    if (res.status == 200) {
      getPendingChallenges()
    }
  } catch (error) {
    console.log(error)
  }
}

getAcceptedChallenges()
getPendingChallenges()
getCreatedChallenges()
</script>