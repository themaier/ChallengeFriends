<template>
     <div v-for="challenge in challenges" :key="challenge.id" class="modal fade modal-md" :id="'comment' + challenge.id" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h2 class="modal-title h5" id="exampleModalLabel">Kommentare</h2>
                    <button class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <ul style="max-height:500px; overflow: auto; " class="px-0 d-flex flex-column gap-3">
                        <li v-for="comment in challenge.comments" :key="comment.id" class="d-flex">
                            <span class="fw-bold  col-4">{{comment.username}}</span>
                            <div class="col-8 d-flex flex-column gap-2 u.overflow-hidden">
                                <img v-if="comment.image_path" class="rounded" :src="IMG_URL + comment.image_path">
                                <span v-if="comment.text">{{comment.text}}</span>
                            </div>
                        </li>
                    </ul>
                    <form @submit.prevent="addComment(challenge.id)">
                        <div class="mb-3">
                            <textarea class="form-control" id="exampleFormControlTextarea1" aria-label="Kommentieren" placeholder="Kommentieren..." rows="3" v-model="commentText"></textarea>
                            <input class="form-control" id="formFile" type="file" name="image" accept="image/png, image/jpg, image/jpeg" capture="user" @change="onFileChanged($event)">
                        </div>
                        <button class="btn btn-primary">Kommentieren</button>   	
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps } from 'vue';
import challengeService from '../services/challenge.service.js'
import {useStore} from '../stores/store'
const store = useStore()
const ipv4 = import.meta.env.VITE_IPV4 || 'localhost';
const IMG_URL = `http://${ipv4}:8000/resources/`
const { challenges } = defineProps(['challenges']);

const commentText = ref(null)
const file = ref(null)
const emit = defineEmits('commentedSucessfully')
const onFileChanged = (e) => {
  file.value = e.target.files[0]
}
const addComment = async (id) => {
    try {
        if(!commentText.value && !file.value) return
        const res = await challengeService.addComment(id, store.user.id, commentText.value, file.value)
        if (res.status == 200) {
            file.value = null
            document.querySelector('#formFile').value = null
            commentText.value = null
            emit('commentedSucessfully')
        }
    } catch (error) {
        console.log(error)
    }
}
</script>

<style scoped lang="scss">
img {
    max-height:900px; 
    object-fit:contain; 
}
</style>