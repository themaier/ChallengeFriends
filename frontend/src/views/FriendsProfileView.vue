<template>
    <div class="container-md">
        <h1 class="my-4">{{username}} - Abgeschlossene Challenges</h1>
        <div class="p-3">
            <div class="d-flex flex-column align-items-center gap-3">
                <div v-for="challenge in challenges" :key="challenge" class="d-flex rounded bg-body flex-column w-100 py-2 u--overflow-hidden" style="max-width: 470px;">
                    <div class="px-2 mb-2 d-flex justify-content-between">
                        <span class="fw-bold">{{challenge.receiver_name}}</span>
                        <span>{{formatDate(challenge.done_date)}}</span>
                    </div>
                    <img v-if="!store.isVideo(challenge.prove_resource_path)" class="rounded" style="max-height:900px;" :src="IMG_URL + challenge.prove_resource_path">
                    <video v-else class="rounded" style="max-height:900px;" controls>
                        <source :src="IMG_URL + challenge.prove_resource_path" type="video/mp4">
                    </video>
                    <div class=" px-1 py-2 d-flex">
                        <LikeButton :challenge="challenge"></LikeButton>
                        <button class="btn icon icon--comment icon--size-1-5 icon--button" data-bs-toggle="modal" :data-bs-target="'#comment'+ challenge.id">{{challenge.comments.length}}</button>
                        <button class="btn icon icon--share icon--size-1-5 icon--button ms-auto" data-bs-toggle="modal" :data-bs-target="'#share'+ challenge.id"></button>
                        <ShareSection :challenge="challenge"></ShareSection>
                    </div>
                    <div class="px-2 fw-bold">{{ challenge.title }}</div>
                    <div class="px-2">{{ challenge.description }}</div>
                    <div v-if="challenge.reward" class="px-2">Reward: {{ challenge.reward }}</div>
                    <div v-if="challenge.hashtags" class="px-2"><a v-for="hashtag in challenge.hashtags" :href="'?'+ hashtag.text" :key="hashtag.id" class="link-primary link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover">#{{hashtag.text}}</a></div>
                </div>
            </div>
        </div>
    </div>

<CommentSection :challenges="challenges" @commentedSucessfully="commentedSucessfully()"></CommentSection>
</template>

<script setup>
import { ref } from 'vue'
import challengeService from '../services/challenge.service.js'
import {useStore} from '../stores/store'
import CommentSection from '../components/CommentSection.vue'
import { useRouter, useRoute } from 'vue-router'
import userService from '../services/user.service.js'
import LikeButton from '../components/LikeButton.vue'
import ShareSection from '../components/ShareSection.vue'

const ipv4 = import.meta.env.VITE_IPV4 || 'localhost';
const IMG_URL = `http://${ipv4}:8000/resources/`
const route = useRoute()
const store = useStore()
const challenges = ref([])
const username = ref('')

const commentedSucessfully = () => {
  getCompletedChallengesByUser(route.params.id)
}

const formatDate = (dateString) => {
  const options = { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' };
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('de-DE', options).format(date);
};

const getCompletedChallengesByUser = async (id) => {

    try {
        const response = await challengeService.getCompletedChallengesByUser(id, store.user.id)
        if (response.status == 200) {
            challenges.value = response.data
        }
    } catch (error) {
        challenges.value = []
    }
}

const getUsername = async (id) => {
    try {
        const response = await userService.getUser(id)
        if (response.status == 200) {
            username.value =  response.data.username
        }
    } catch (error) {
        username.value = ''
    }
}

getCompletedChallengesByUser(route.params.id)
getUsername(route.params.id)

</script>