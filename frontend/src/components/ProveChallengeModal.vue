<template>
    <div ref="modalRef" v-for="challenge in challenges" :key="challenge.id" class="modal fade" :id="'proveModal' + challenge.id" tabindex="-1" aria-labelledby="challengeFinishLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h2 class="modal-title h5" id="challengeFinishLabel">Challenge abschließen</h2>
                    <button class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="completeChallenge(challenge.id, file)">
                      <div class="mb-3">
                        <label for="formFile" class="form-label">Foto oder Video hochladen</label>
                        <input class="form-control" id="formFile" type="file" name="image" accept="image/png, image/jpg, image/jpeg, video/mp4" capture="user" @change="onFileChanged($event)">
                      </div>
                      <button class="btn btn-primary" >Senden</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps } from 'vue';
import  {Modal} from 'bootstrap'
import challengeService from '../services/challenge.service.js'
let { challenges} = defineProps(['challenges']);
const file = ref(null)
    const modalRef = ref(null);
const emit = defineEmits('uploadedSucessfully')

const onFileChanged = (e) => {
  file.value = e.target.files[0]
}

const completeChallenge = async (id) => {
    try {
        if(!file.value) return
        const res = await challengeService.completeChallenge(id, file.value)
        if (res.status == 200) {
            file.value = null
            document.querySelector('#formFile').value = null
            const myModalElement = modalRef.value[0]
            const bootstrapModal = Modal.getInstance(modalRef.value[0]);
            myModalElement.addEventListener('hidden.bs.modal', event => {
                emit('uploadedSucessfully')
            })
            bootstrapModal.hide();
        }
    } catch (error) {
        console.log(error)
    }
}
</script>
