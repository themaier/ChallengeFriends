<template>
    <button  @click="likeChallenge(challenge)" :class="{ 'icon--love--filled': challenge.likes.has_liked }" class="btn icon icon--love icon--size-1-5 icon--button me-2">{{challenge.likes.likes_count}}</button>
</template>

<script setup>
import { useStore } from '../stores/store'
import challengeService from '../services/challenge.service.js'

const store = useStore()
const { challenge } = defineProps(['challenge']);

const likeChallenge = async (challenge) => {
    try {
        const response = await challengeService.likeChallenge(challenge.id, store.user.id)
        if (response.status == 200) {
            challenge.likes.has_liked = !challenge.likes.has_liked
            if(challenge.likes.has_liked) {
                challenge.likes.likes_count = challenge.likes.likes_count + 1
            } else {
                challenge.likes.likes_count = challenge.likes.likes_count - 1
            }
        }
    } catch (error) {
        console.log(error)
    }
}
</script>
