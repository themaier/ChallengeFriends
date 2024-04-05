import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useStore = defineStore('store', () => {
  const loggedIn = ref(localStorage.getItem('loggedIn') === 'true')
  const user = ref(JSON.parse(localStorage.getItem('user')))
  const challengeId = ref(localStorage.getItem('challengeId'))
  const isVideo = (resourcePath) => {
    const videoExtensions = ['mp4']; 
    const extension = resourcePath.toLowerCase().split('.').pop();
    return videoExtensions.includes(extension);
  }

  return { loggedIn, user, challengeId, isVideo}
})
