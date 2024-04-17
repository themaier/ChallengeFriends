<template>
    <div ref="linkModal" class="modal fade" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="staticBackdropLabel">Challenge Link</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          {{ipv4}}?challengeId={{unlinkedChallengeId}}
        </div>
        <div class="modal-footer d-flex justify-content-center">
          <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="copyTextToClipboard()">Kopieren</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { Modal } from 'bootstrap';
const ipv4 = import.meta.env.VITE_IPV4 || 'http://localhost:3000';
const linkModal = ref(null);
const unlinkedChallengeId = ref('')

const showLinkModal = (challengeId) => {
    unlinkedChallengeId.value = challengeId
    new Modal(linkModal.value).show();
};

const copyTextToClipboard = () => {
  navigator.clipboard.writeText(`${ipv4}?challengeId=${unlinkedChallengeId.value}`).then(function() {
  }).catch(err => {
    console.error('Error in copying link: ', err);
  });
}

defineExpose({
    showLinkModal
});

</script>