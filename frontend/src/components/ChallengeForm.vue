<template>
  <div class="d-flex flex-column align-items-center">
    <button class="btn btn-primary" @click="isCollapsed = !isCollapsed" style="border-radius: 20px; background: linear-gradient(to right, #6a11cb, #2575fc); padding: 0.75rem 2rem;">
      Challenge erstellen <i :class="isFormVisible ? 'bi bi-chevron-up' : 'bi bi-chevron-down' " class="ms-2"></i>
    </button>

    <div :class="{'collapse': isCollapsed, 'show': !isCollapsed, 'w-100': true, 'mt-3': true}">
      <div class="card card-body" style="border-radius: 20px;">
        <form @submit.prevent="submitForm">
          <div class="mb-3">
            <label for="challengeName" class="form-label">Challenge Name</label>
            <input type="text" id="challengeName" class="form-control" v-model="form.challengeName" required>
          </div>
          <div class="mb-3">
            <label for="description" class="form-label">Description</label>
            <textarea id="description" class="form-control" v-model="form.description" required></textarea>
          </div>
          <button type="submit" class="btn btn-success">Submit</button>
        </form>
      </div>
    </div>
  </div>
</template>
  
<script setup>
import { ref } from 'vue';
const isCollapsed = ref(true);

const form = ref({
  challengeName: '',
  description: '',
});
const isFormVisible = ref(false);

const submitForm = () => {
  console.log("Form data:", form.value);
};
</script>
  
<style scoped>
/* Add any component-specific styles here */
</style>